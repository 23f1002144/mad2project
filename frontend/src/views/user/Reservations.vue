<template>
  <div class="container-fluid mt-4">
    <!-- Page Header -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center">
          <h2>My Reservations</h2>
          <div class="d-flex gap-2">
            <button @click="refreshReservations" class="btn btn-outline-primary" :disabled="loading">
              <i class="fas fa-sync-alt me-2" :class="{ 'fa-spin': loading }"></i>
              Refresh
            </button>
            <router-link to="/parking-lots" class="btn btn-primary">
              <i class="fas fa-plus me-2"></i>
              New Reservation
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Filter and Status Cards -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="card">
          <div class="card-body">
            <div class="row">
              <div class="col-md-4 mb-3">
                <label for="statusFilter" class="form-label">Filter by Status</label>
                <select class="form-select" id="statusFilter" v-model="statusFilter">
                  <option value="">All Reservations</option>
                  <option value="reserved">Reserved</option>
                  <option value="active">Active</option>
                  <option value="completed">Completed</option>
                  <option value="cancelled">Cancelled</option>
                </select>
              </div>
              
              <div class="col-md-4 mb-3">
                <label for="dateFrom" class="form-label">From Date</label>
                <input
                  type="date"
                  class="form-control"
                  id="dateFrom"
                  v-model="dateFrom"
                />
              </div>
              
              <div class="col-md-4 mb-3">
                <label for="dateTo" class="form-label">To Date</label>
                <input
                  type="date"
                  class="form-control"
                  id="dateTo"
                  v-model="dateTo"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Stats -->
    <div class="row mb-4">
      <div class="col-md-3 col-sm-6 mb-3">
        <div class="card text-center stats-card bg-warning text-dark">
          <div class="card-body">
            <i class="fas fa-clock fa-2x mb-2"></i>
            <h4 class="mb-1">{{ stats.reserved }}</h4>
            <p class="mb-0">Reserved</p>
          </div>
        </div>
      </div>
      
      <div class="col-md-3 col-sm-6 mb-3">
        <div class="card text-center stats-card bg-success text-white">
          <div class="card-body">
            <i class="fas fa-car fa-2x mb-2"></i>
            <h4 class="mb-1">{{ stats.active }}</h4>
            <p class="mb-0">Active</p>
          </div>
        </div>
      </div>
      
      <div class="col-md-3 col-sm-6 mb-3">
        <div class="card text-center stats-card bg-info text-white">
          <div class="card-body">
            <i class="fas fa-check-circle fa-2x mb-2"></i>
            <h4 class="mb-1">{{ stats.completed }}</h4>
            <p class="mb-0">Completed</p>
          </div>
        </div>
      </div>
      
      <div class="col-md-3 col-sm-6 mb-3">
        <div class="card text-center stats-card bg-danger text-white">
          <div class="card-body">
            <i class="fas fa-times-circle fa-2x mb-2"></i>
            <h4 class="mb-1">{{ stats.cancelled }}</h4>
            <p class="mb-0">Cancelled</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3 text-muted">Loading reservations...</p>
    </div>

    <!-- No Reservations -->
    <div v-else-if="filteredReservations.length === 0" class="text-center py-5">
      <i class="fas fa-calendar-times fa-3x text-muted mb-3"></i>
      <h4 class="text-muted">No reservations found</h4>
      <p class="text-muted mb-4">
        {{ statusFilter ? 'No reservations match your filter criteria.' : 'You haven\'t made any reservations yet.' }}
      </p>
      <router-link to="/parking-lots" class="btn btn-primary">
        <i class="fas fa-search me-2"></i>
        Find Parking
      </router-link>
    </div>

    <!-- Reservations List -->
    <div v-else class="row">
      <div v-for="reservation in filteredReservations" :key="reservation.id" class="col-lg-6 col-xl-4 mb-4">
        <div class="card h-100 reservation-card">
          <div class="card-header d-flex justify-content-between align-items-start">
            <h6 class="mb-0 text-primary">{{ reservation.parking_lot_name }}</h6>
            <span 
              class="badge"
              :class="{
                'bg-warning': reservation.status === 'reserved',
                'bg-success': reservation.status === 'active',
                'bg-info': reservation.status === 'completed',
                'bg-danger': reservation.status === 'cancelled'
              }"
            >
              {{ formatStatus(reservation.status) }}
            </span>
          </div>
          
          <div class="card-body">
            <div class="mb-3">
              <p class="mb-1">
                <i class="fas fa-map-marker-alt me-2 text-muted"></i>
                <strong>Spot:</strong> {{ reservation.spot_number }}
              </p>
              <p class="mb-1">
                <i class="fas fa-car me-2 text-muted"></i>
                <strong>Vehicle:</strong> {{ reservation.vehicle_number || 'N/A' }}
              </p>
              <p class="mb-1">
                <i class="fas fa-calendar me-2 text-muted"></i>
                <strong>Reserved:</strong> {{ formatDateTime(reservation.reservation_timestamp) }}
              </p>
            </div>

            <div v-if="reservation.parking_timestamp" class="mb-3">
              <p class="mb-1">
                <i class="fas fa-clock me-2 text-muted"></i>
                <strong>Parked:</strong> {{ formatDateTime(reservation.parking_timestamp) }}
              </p>
              <p v-if="reservation.leaving_timestamp" class="mb-1">
                <i class="fas fa-sign-out-alt me-2 text-muted"></i>
                <strong>Left:</strong> {{ formatDateTime(reservation.leaving_timestamp) }}
              </p>
            </div>

            <div class="mb-3">
              <div class="row">
                <div class="col-6">
                  <div class="text-center">
                    <div class="h6 text-primary mb-0">{{ reservation.duration_hours || 0 }}h</div>
                    <small class="text-muted">Duration</small>
                  </div>
                </div>
                <div class="col-6">
                  <div class="text-center">
                    <div class="h6 text-success mb-0">${{ reservation.parking_cost || 0 }}</div>
                    <small class="text-muted">Cost</small>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="reservation.remarks" class="mb-3">
              <p class="small text-muted mb-0">
                <i class="fas fa-comment me-2"></i>
                {{ reservation.remarks }}
              </p>
            </div>
          </div>

          <div class="card-footer bg-transparent">
            <div class="d-flex gap-2">
              <!-- Start Parking (for reserved status) -->
              <button
                v-if="reservation.status === 'reserved'"
                @click="startParking(reservation)"
                class="btn btn-success btn-sm flex-fill"
                :disabled="actionLoading === reservation.id"
              >
                <span v-if="actionLoading === reservation.id" class="spinner-border spinner-border-sm me-1"></span>
                Start Parking
              </button>

              <!-- End Parking (for active status) -->
              <button
                v-if="reservation.status === 'active'"
                @click="endParking(reservation)"
                class="btn btn-warning btn-sm flex-fill"
                :disabled="actionLoading === reservation.id"
              >
                <span v-if="actionLoading === reservation.id" class="spinner-border spinner-border-sm me-1"></span>
                End Parking
              </button>

              <!-- Cancel Reservation -->
              <button
                v-if="['reserved', 'active'].includes(reservation.status)"
                @click="cancelReservation(reservation)"
                class="btn btn-outline-danger btn-sm"
                :disabled="actionLoading === reservation.id"
              >
                <i class="fas fa-times"></i>
              </button>

              <!-- View Details -->
              <button
                @click="viewDetails(reservation)"
                class="btn btn-outline-primary btn-sm"
                :class="{ 'flex-fill': !['reserved', 'active'].includes(reservation.status) }"
              >
                <i class="fas fa-eye"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Reservation Details Modal -->
    <div class="modal fade" id="detailsModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Reservation Details</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div v-if="selectedReservation">
              <div class="row mb-3">
                <div class="col-md-6">
                  <h6>Basic Information</h6>
                  <p><strong>Reservation ID:</strong> #{{ selectedReservation.id }}</p>
                  <p><strong>Parking Lot:</strong> {{ selectedReservation.parking_lot_name }}</p>
                  <p><strong>Spot Number:</strong> {{ selectedReservation.spot_number }}</p>
                  <p><strong>Vehicle:</strong> {{ selectedReservation.vehicle_number || 'N/A' }}</p>
                  <p><strong>Status:</strong> 
                    <span 
                      class="badge"
                      :class="{
                        'bg-warning': selectedReservation.status === 'reserved',
                        'bg-success': selectedReservation.status === 'active',
                        'bg-info': selectedReservation.status === 'completed',
                        'bg-danger': selectedReservation.status === 'cancelled'
                      }"
                    >
                      {{ formatStatus(selectedReservation.status) }}
                    </span>
                  </p>
                </div>
                
                <div class="col-md-6">
                  <h6>Timing Information</h6>
                  <p><strong>Reserved At:</strong> {{ formatDateTime(selectedReservation.reservation_timestamp) }}</p>
                  <p v-if="selectedReservation.parking_timestamp">
                    <strong>Parked At:</strong> {{ formatDateTime(selectedReservation.parking_timestamp) }}
                  </p>
                  <p v-if="selectedReservation.leaving_timestamp">
                    <strong>Left At:</strong> {{ formatDateTime(selectedReservation.leaving_timestamp) }}
                  </p>
                  <p><strong>Duration:</strong> {{ selectedReservation.duration_hours || 0 }} hours</p>
                  <p><strong>Total Cost:</strong> ${{ selectedReservation.parking_cost || 0 }}</p>
                </div>
              </div>
              
              <div v-if="selectedReservation.remarks" class="mb-3">
                <h6>Remarks</h6>
                <p class="text-muted">{{ selectedReservation.remarks }}</p>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'UserReservations',
  data() {
    return {
      loading: false,
      actionLoading: null,
      reservations: [],
      statusFilter: '',
      dateFrom: '',
      dateTo: '',
      selectedReservation: null,
      stats: {
        reserved: 0,
        active: 0,
        completed: 0,
        cancelled: 0
      }
    }
  },
  computed: {
    filteredReservations() {
      let filtered = this.reservations
      
      // Filter by status
      if (this.statusFilter) {
        filtered = filtered.filter(r => r.status === this.statusFilter)
      }
      
      // Filter by date range
      if (this.dateFrom) {
        filtered = filtered.filter(r => {
          const reservationDate = new Date(r.reservation_timestamp).toISOString().split('T')[0]
          return reservationDate >= this.dateFrom
        })
      }
      
      if (this.dateTo) {
        filtered = filtered.filter(r => {
          const reservationDate = new Date(r.reservation_timestamp).toISOString().split('T')[0]
          return reservationDate <= this.dateTo
        })
      }
      
      // Sort by creation date (newest first)
      return filtered.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    }
  },
  async mounted() {
    await this.loadReservations()
  },
  methods: {
    ...mapActions('reservations', ['fetchUserReservations', 'updateReservationStatus', 'cancelUserReservation']),
    
    async loadReservations() {
      this.loading = true
      try {
        this.reservations = await this.fetchUserReservations()
        this.calculateStats()
      } catch (error) {
        console.error('Error loading reservations:', error)
        this.$toast?.error('Failed to load reservations')
      } finally {
        this.loading = false
      }
    },
    
    calculateStats() {
      this.stats = {
        reserved: this.reservations.filter(r => r.status === 'reserved').length,
        active: this.reservations.filter(r => r.status === 'active').length,
        completed: this.reservations.filter(r => r.status === 'completed').length,
        cancelled: this.reservations.filter(r => r.status === 'cancelled').length
      }
    },
    
    async refreshReservations() {
      await this.loadReservations()
    },
    
    async startParking(reservation) {
      this.actionLoading = reservation.id
      try {
        await this.updateReservationStatus({
          id: reservation.id,
          status: 'active',
          parking_timestamp: new Date().toISOString()
        })
        
        await this.loadReservations()
        this.$toast?.success('Parking started successfully!')
        
      } catch (error) {
        console.error('Error starting parking:', error)
        this.$toast?.error('Failed to start parking')
      } finally {
        this.actionLoading = null
      }
    },
    
    async endParking(reservation) {
      this.actionLoading = reservation.id
      try {
        await this.updateReservationStatus({
          id: reservation.id,
          status: 'completed',
          leaving_timestamp: new Date().toISOString()
        })
        
        await this.loadReservations()
        this.$toast?.success('Parking ended successfully!')
        
      } catch (error) {
        console.error('Error ending parking:', error)
        this.$toast?.error('Failed to end parking')
      } finally {
        this.actionLoading = null
      }
    },
    
    async cancelReservation(reservation) {
      if (!confirm('Are you sure you want to cancel this reservation?')) {
        return
      }
      
      this.actionLoading = reservation.id
      try {
        await this.cancelUserReservation(reservation.id)
        await this.loadReservations()
        this.$toast?.success('Reservation cancelled successfully!')
        
      } catch (error) {
        console.error('Error cancelling reservation:', error)
        this.$toast?.error('Failed to cancel reservation')
      } finally {
        this.actionLoading = null
      }
    },
    
    viewDetails(reservation) {
      this.selectedReservation = reservation
      const modal = new window.bootstrap.Modal(document.getElementById('detailsModal'))
      modal.show()
    },
    
    formatStatus(status) {
      const statusMap = {
        'reserved': 'Reserved',
        'active': 'Active',
        'completed': 'Completed',
        'cancelled': 'Cancelled'
      }
      return statusMap[status] || status
    },
    
    formatDateTime(dateString) {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleString()
    }
  }
}
</script>

<style scoped>
.reservation-card {
  border: none;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: transform 0.2s, box-shadow 0.2s;
  border-radius: 12px;
}

.reservation-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}

.stats-card {
  border: none;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  border-radius: 12px;
  transition: transform 0.2s;
}

.stats-card:hover {
  transform: translateY(-2px);
}

.card-header {
  border-bottom: 1px solid #e9ecef;
  border-radius: 12px 12px 0 0;
}

.card-footer {
  border-top: 1px solid #e9ecef;
  border-radius: 0 0 12px 12px;
}

.badge {
  font-size: 0.75rem;
  padding: 0.5em 0.75em;
}

.btn {
  border-radius: 8px;
  font-weight: 500;
}

.btn-sm {
  font-size: 0.8rem;
}

.modal-content {
  border-radius: 12px;
  border: none;
}

.fa-spin {
  animation: fa-spin 1s infinite linear;
}

@keyframes fa-spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
