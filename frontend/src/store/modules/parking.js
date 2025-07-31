import api from '@/services/api'

export default {
    namespaced: true,

    state: {
        parkingLots: [],
        currentReservation: null,
        reservationHistory: [],
        dashboardData: {}
    },

    mutations: {
        SET_PARKING_LOTS(state, lots) {
            state.parkingLots = lots
        },

        SET_CURRENT_RESERVATION(state, reservation) {
            state.currentReservation = reservation
        },

        SET_RESERVATION_HISTORY(state, history) {
            state.reservationHistory = history
        },

        SET_DASHBOARD_DATA(state, data) {
            state.dashboardData = data
        },

        ADD_RESERVATION(state, reservation) {
            state.reservationHistory.unshift(reservation)
            if (reservation.status === 'active' || reservation.status === 'reserved') {
                state.currentReservation = reservation
            }
        },

        UPDATE_RESERVATION(state, updatedReservation) {
            // Update in history
            const index = state.reservationHistory.findIndex(r => r.id === updatedReservation.id)
            if (index !== -1) {
                state.reservationHistory.splice(index, 1, updatedReservation)
            }

            // Update current reservation
            if (state.currentReservation && state.currentReservation.id === updatedReservation.id) {
                if (updatedReservation.status === 'completed' || updatedReservation.status === 'cancelled') {
                    state.currentReservation = null
                } else {
                    state.currentReservation = updatedReservation
                }
            }
        }
    },

    actions: {
        async fetchParkingLots({ commit, dispatch }) {
            try {
                const response = await api.get('/user/parking-lots')
                commit('SET_PARKING_LOTS', response.data.parking_lots)
                return response.data.parking_lots
            } catch (error) {
                const message = error.response?.data?.error || 'Failed to fetch parking lots'
                dispatch('showAlert', { message, type: 'danger' }, { root: true })
                throw error
            }
        },

        async fetchDashboardData({ commit, dispatch }) {
            try {
                const response = await api.get('/user/dashboard')
                commit('SET_DASHBOARD_DATA', response.data)
                commit('SET_CURRENT_RESERVATION', response.data.active_reservation)
                commit('SET_RESERVATION_HISTORY', response.data.recent_reservations)
                return response.data
            } catch (error) {
                const message = error.response?.data?.error || 'Failed to fetch dashboard data'
                dispatch('showAlert', { message, type: 'danger' }, { root: true })
                throw error
            }
        },

        async createReservation({ commit, dispatch }, { lotId, vehicleNumber, remarks }) {
            try {
                dispatch('setLoading', true, { root: true })

                const response = await api.post('/user/reservations', {
                    lot_id: lotId,
                    vehicle_number: vehicleNumber,
                    remarks
                })

                commit('ADD_RESERVATION', response.data.reservation)

                dispatch('showAlert', {
                    message: 'Reservation created successfully!',
                    type: 'success'
                }, { root: true })

                return response.data.reservation
            } catch (error) {
                const message = error.response?.data?.error || 'Failed to create reservation'
                dispatch('showAlert', { message, type: 'danger' }, { root: true })
                throw error
            } finally {
                dispatch('setLoading', false, { root: true })
            }
        },

        async parkVehicle({ commit, dispatch }, reservationId) {
            try {
                dispatch('setLoading', true, { root: true })

                const response = await api.post(`/user/reservations/${reservationId}/park`)

                commit('UPDATE_RESERVATION', response.data.reservation)

                dispatch('showAlert', {
                    message: 'Vehicle parked successfully!',
                    type: 'success'
                }, { root: true })

                return response.data.reservation
            } catch (error) {
                const message = error.response?.data?.error || 'Failed to park vehicle'
                dispatch('showAlert', { message, type: 'danger' }, { root: true })
                throw error
            } finally {
                dispatch('setLoading', false, { root: true })
            }
        },

        async releaseParking({ commit, dispatch }, reservationId) {
            try {
                dispatch('setLoading', true, { root: true })

                const response = await api.post(`/user/reservations/${reservationId}/release`)

                commit('UPDATE_RESERVATION', response.data.reservation)

                dispatch('showAlert', {
                    message: 'Parking released successfully!',
                    type: 'success'
                }, { root: true })

                return response.data.reservation
            } catch (error) {
                const message = error.response?.data?.error || 'Failed to release parking'
                dispatch('showAlert', { message, type: 'danger' }, { root: true })
                throw error
            } finally {
                dispatch('setLoading', false, { root: true })
            }
        },

        async fetchReservationHistory({ commit, dispatch }, { page = 1, perPage = 10, status = null }) {
            try {
                const params = { page, per_page: perPage }
                if (status) params.status = status

                const response = await api.get('/user/reservations', { params })

                if (page === 1) {
                    commit('SET_RESERVATION_HISTORY', response.data.reservations)
                }

                return response.data
            } catch (error) {
                const message = error.response?.data?.error || 'Failed to fetch reservation history'
                dispatch('showAlert', { message, type: 'danger' }, { root: true })
                throw error
            }
        },

        async exportReservations({ dispatch }) {
            try {
                dispatch('setLoading', true, { root: true })

                const response = await api.get('/analytics/export/user-data')

                // Convert data to CSV and trigger download
                const csvData = response.data.export_data
                const csv = convertToCSV(csvData)
                downloadCSV(csv, 'my-parking-history.csv')

                dispatch('showAlert', {
                    message: 'Export completed successfully!',
                    type: 'success'
                }, { root: true })

                return response.data
            } catch (error) {
                const message = error.response?.data?.error || 'Failed to export data'
                dispatch('showAlert', { message, type: 'danger' }, { root: true })
                throw error
            } finally {
                dispatch('setLoading', false, { root: true })
            }
        }
    },

    getters: {
        hasActiveReservation: state => !!state.currentReservation,
        completedReservations: state => state.reservationHistory.filter(r => r.status === 'completed'),
        totalSpent: (state, getters) => {
            return getters.completedReservations.reduce((total, r) => total + (r.parking_cost || 0), 0)
        }
    }
}

// Helper functions
function convertToCSV(data) {
    if (!data.length) return ''

    const headers = Object.keys(data[0])
    const csvContent = [
        headers.join(','),
        ...data.map(row => headers.map(header => {
            const value = row[header]
            return typeof value === 'string' && value.includes(',') ? `"${value}"` : value
        }).join(','))
    ].join('\n')

    return csvContent
}

function downloadCSV(csv, filename) {
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
    const link = document.createElement('a')

    if (link.download !== undefined) {
        const url = URL.createObjectURL(blob)
        link.setAttribute('href', url)
        link.setAttribute('download', filename)
        link.style.visibility = 'hidden'
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
    }
}
