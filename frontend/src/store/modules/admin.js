import api from '@/services/api'

export default {
    namespaced: true,

    state: {
        dashboardStats: {},
        parkingLots: [],
        users: [],
        reservations: [],
        analytics: {}
    },

    mutations: {
        SET_DASHBOARD_STATS(state, stats) {
            state.dashboardStats = stats
        },

        SET_PARKING_LOTS(state, lots) {
            state.parkingLots = lots
        },

        SET_USERS(state, users) {
            state.users = users
        },

        SET_RESERVATIONS(state, reservations) {
            state.reservations = reservations
        },

        SET_ANALYTICS(state, analytics) {
            state.analytics = analytics
        },

        ADD_PARKING_LOT(state, lot) {
            state.parkingLots.push(lot)
        },

        UPDATE_PARKING_LOT(state, updatedLot) {
            const index = state.parkingLots.findIndex(lot => lot.id === updatedLot.id)
            if (index !== -1) {
                state.parkingLots.splice(index, 1, updatedLot)
            }
        },

        REMOVE_PARKING_LOT(state, lotId) {
            state.parkingLots = state.parkingLots.filter(lot => lot.id !== lotId)
        }
    },

    actions: {
        async fetchDashboardStats({ commit, dispatch }) {
            try {
                const response = await api.get('/admin/dashboard')
                commit('SET_DASHBOARD_STATS', response.data)
                return response.data
            } catch (error) {
                const message = error.response?.data?.error || 'Failed to fetch dashboard stats'
                dispatch('showAlert', { message, type: 'danger' }, { root: true })
                throw error
            }
        },

        async fetchParkingLots({ commit, dispatch }) {
            try {
                const response = await api.get('/admin/parking-lots')
                commit('SET_PARKING_LOTS', response.data.parking_lots)
                return response.data.parking_lots
            } catch (error) {
                const message = error.response?.data?.error || 'Failed to fetch parking lots'
                dispatch('showAlert', { message, type: 'danger' }, { root: true })
                throw error
            }
        },

        async createParkingLot({ commit, dispatch }, lotData) {
            try {
                dispatch('setLoading', true, { root: true })

                const response = await api.post('/admin/parking-lots', lotData)

                commit('ADD_PARKING_LOT', response.data.parking_lot)

                dispatch('showAlert', {
                    message: 'Parking lot created successfully!',
                    type: 'success'
                }, { root: true })

                return response.data.parking_lot
            } catch (error) {
                const message = error.response?.data?.error || 'Failed to create parking lot'
                dispatch('showAlert', { message, type: 'danger' }, { root: true })
                throw error
            } finally {
                dispatch('setLoading', false, { root: true })
            }
        },

        async updateParkingLot({ commit, dispatch }, { lotId, lotData }) {
            try {
                dispatch('setLoading', true, { root: true })

                const response = await api.put(`/admin/parking-lots/${lotId}`, lotData)

                commit('UPDATE_PARKING_LOT', response.data.parking_lot)

                dispatch('showAlert', {
                    message: 'Parking lot updated successfully!',
                    type: 'success'
                }, { root: true })

                return response.data.parking_lot
            } catch (error) {
                const message = error.response?.data?.error || 'Failed to update parking lot'
                dispatch('showAlert', { message, type: 'danger' }, { root: true })
                throw error
            } finally {
                dispatch('setLoading', false, { root: true })
            }
        },

        async deleteParkingLot({ commit, dispatch }, lotId) {
            try {
                dispatch('setLoading', true, { root: true })

                await api.delete(`/admin/parking-lots/${lotId}`)

                commit('REMOVE_PARKING_LOT', lotId)

                dispatch('showAlert', {
                    message: 'Parking lot deleted successfully!',
                    type: 'success'
                }, { root: true })

            } catch (error) {
                const message = error.response?.data?.error || 'Failed to delete parking lot'
                dispatch('showAlert', { message, type: 'danger' }, { root: true })
                throw error
            } finally {
                dispatch('setLoading', false, { root: true })
            }
        },

        async fetchUsers({ commit, dispatch }, { page = 1, perPage = 10 }) {
            try {
                const response = await api.get('/admin/users', {
                    params: { page, per_page: perPage }
                })

                commit('SET_USERS', response.data.users)
                return response.data
            } catch (error) {
                const message = error.response?.data?.error || 'Failed to fetch users'
                dispatch('showAlert', { message, type: 'danger' }, { root: true })
                throw error
            }
        },

        async fetchAllUsers({ commit, dispatch }) {
            try {
                const response = await api.get('/admin/users', {
                    params: { per_page: 1000 } // Get all users
                })

                commit('SET_USERS', response.data.users)
                return response.data.users
            } catch (error) {
                const message = error.response?.data?.error || 'Failed to fetch all users'
                dispatch('showAlert', { message, type: 'danger' }, { root: true })
                throw error
            }
        },

        async updateUserStatus({ dispatch }, { id, is_active }) {
            try {
                const response = await api.put(`/admin/users/${id}`, { is_active })

                dispatch('showAlert', {
                    message: `User ${is_active ? 'activated' : 'deactivated'} successfully!`,
                    type: 'success'
                }, { root: true })

                return response.data.user
            } catch (error) {
                const message = error.response?.data?.error || 'Failed to update user status'
                dispatch('showAlert', { message, type: 'danger' }, { root: true })
                throw error
            }
        },

        async fetchUserReservations({ dispatch }, userId) {
            try {
                const response = await api.get(`/admin/users/${userId}/reservations`)
                return response.data.reservations
            } catch (error) {
                const message = error.response?.data?.error || 'Failed to fetch user reservations'
                dispatch('showAlert', { message, type: 'danger' }, { root: true })
                throw error
            }
        },

        async fetchReservations({ commit, dispatch }, { page = 1, perPage = 20, status = null }) {
            try {
                const params = { page, per_page: perPage }
                if (status) params.status = status

                const response = await api.get('/admin/reservations', { params })

                commit('SET_RESERVATIONS', response.data.reservations)
                return response.data
            } catch (error) {
                const message = error.response?.data?.error || 'Failed to fetch reservations'
                dispatch('showAlert', { message, type: 'danger' }, { root: true })
                throw error
            }
        },

        async fetchParkingSpots({ dispatch }, lotId) {
            try {
                const response = await api.get(`/admin/parking-lots/${lotId}/spots`)
                return response.data
            } catch (error) {
                const message = error.response?.data?.error || 'Failed to fetch parking spots'
                dispatch('showAlert', { message, type: 'danger' }, { root: true })
                throw error
            }
        },

        async fetchAnalytics({ commit, dispatch }) {
            try {
                const response = await api.get('/analytics/dashboard')
                commit('SET_ANALYTICS', response.data)
                return response.data
            } catch (error) {
                const message = error.response?.data?.error || 'Failed to fetch analytics'
                dispatch('showAlert', { message, type: 'danger' }, { root: true })
                throw error
            }
        },

        async fetchLotAnalytics({ dispatch }, lotId) {
            try {
                const response = await api.get(`/analytics/lots/${lotId}/analytics`)
                return response.data
            } catch (error) {
                const message = error.response?.data?.error || 'Failed to fetch lot analytics'
                dispatch('showAlert', { message, type: 'danger' }, { root: true })
                throw error
            }
        }
    },

    getters: {
        totalRevenue: state => state.dashboardStats.statistics?.total_revenue || 0,
        totalUsers: state => state.dashboardStats.statistics?.total_users || 0,
        totalLots: state => state.dashboardStats.statistics?.total_lots || 0,
        occupancyRate: state => {
            const stats = state.dashboardStats.statistics
            if (!stats || !stats.total_spots) return 0
            return ((stats.occupied_spots / stats.total_spots) * 100).toFixed(1)
        },
        availableLots: state => state.parkingLots.filter(lot => lot.is_active),
        activeUsers: state => state.users.filter(user => user.is_active)
    }
}
