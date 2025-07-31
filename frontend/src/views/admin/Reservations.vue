<template>
  <div class="container-fluid mt-4">
    <!-- Page Header -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center">
          <h2>Manage Reservations</h2>
          <div class="d-flex gap-2">
            <button @click="refreshReservations" class="btn btn-outline-primary" :disabled="loading">
              <i class="fas fa-sync-alt me-2" :class="{ 'fa-spin': loading }"></i>
              Refresh
            </button>
            <button @click="exportReservations" class="btn btn-outline-success">
              <i class="fas fa-download me-2"></i>
              Export
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Search and Filter -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="card">
          <div class="card-body">
            <div class="row">
              <div class="col-lg-3 col-md-6 mb-3">
                <label for="search" class="form-label">Search</label>
                <input
                  type="text"
                  class="form-control"
                  id="search"
                  v-model="searchQuery"
                  placeholder="Search by user, lot, or vehicle..."
                />
              </div>
              <div class="col-lg-3 col-md-6 mb-3">
                <label for="statusFilter" class="form-label">Status</label>
                <select class="form-select" id="statusFilter" v-model="statusFilter">
                  <option value="">All Status</option>
                  <option value="reserved">Reserved</option>
                  <option value="active">Active</option>
                  <option value="completed">Completed</option>
                  <option value="cancelled">Cancelled</option>
                </select>
              </div>
              <div class="col-lg-3 col-md-6 mb-3">
                <label for="dateFrom" class="form-label">From Date</label>
                <input
                  type="date"
                  class="form-control"
                  id="dateFrom"
                  v-model="dateFrom"
                />
              </div>
              <div class="col-lg-3 col-md-6 mb-3">
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

    <!-- Reservation Statistics -->
    <div class="row mb-4">
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="card text-center stats-card bg-warning text-dark">
          <div class="card-body">
            <i class="fas fa-clock fa-2x mb-2"></i>
            <h3 class="mb-1">{{ stats.reserved }}</h3>
            <p class="mb-0">Reserved</p>
          </div>
        </div>
      </div>
      
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="card text-center stats-card bg-success text-white">
          <div class="card-body">
            <i class="fas fa-car fa-2x mb-2"></i>
            <h3 class="mb-1">{{ stats.active }}</h3>
            <p class="mb-0">Active</p>
          </div>
        </div>
      </div>
      
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="card text-center stats-card bg-info text-white">
          <div class="card-body">
            <i class="fas fa-check-circle fa-2x mb-2"></i>
            <h3 class="mb-1">{{ stats.completed }}</h3>
            <p class="mb-0">Completed</p>
          </div>
        </div>
      </div>
      
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="card text-center stats-card bg-danger text-white">
          <div class="card-body">
            <i class="fas fa-times-circle fa-2x mb-2"></i>
            <h3 class="mb-1">{{ stats.cancelled }}</h3>
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

    <!-- Reservations Table -->
    <div v-else class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">Reservations ({{ filteredReservations.length }})</h5>
          </div>
          <div class="card-body p-0">
            <div v-if="filteredReservations.length === 0" class="text-center py-5">
              <i class="fas fa-calendar-times fa-3x text-muted mb-3"></i>
              <h5 class="text-muted">No reservations found</h5>
              <p class="text-muted">Try adjusting your search criteria.</p>
            </div>
            <div v-else class="table-responsive">
              <table class="table table-hover mb-0">
                <thead class="bg-light">
                  <tr>
                    <th>ID</th>
                    <th>User</th>
                    <th>Parking Lot</th>
                    <th>Spot</th>
                    <th>Vehicle</th>
                    <th>Reserved</th>
                    <th>Duration</th>
                    <th>Cost</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="reservation in paginatedReservations" :key="reservation.id">
                    <td>
                      <span class="fw-bold">#{{ reservation.id }}</span>
                    </td>
                    <td>
                      <div>{{ reservation.user_name }}</div>
                      <small class="text-muted">{{ reservation.user?.email || 'N/A' }}</small>
                    </td>
                    <td>
                      <div class="fw-bold">{{ reservation.parking_lot_name }}</div>
                      <small class="text-muted">{{ reservation.parking_lot?.address || 'N/A' }}</small>
                    </td>
                    <td class="text-center">
                      <span class="badge bg-secondary">{{ reservation.spot_number }}</span>
                    </td>
                    <td>
                      <span class="fw-bold">{{ reservation.vehicle_number || 'N/A' }}</span>
                    </td>
                    <td>
                      <div>{{ formatDate(reservation.reservation_timestamp) }}</div>
                      <small class="text-muted">{{ formatTime(reservation.reservation_timestamp) }}</small>
                    </td>
                    <td class="text-center">
                      <span class="badge bg-info">{{ reservation.duration_hours || 0 }}h</span>
                    </td>
                    <td class="text-center">
                      <span class="fw-bold text-success">${{ reservation.parking_cost || 0 }}</span>
                    </td>
                    <td>
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
                    </td>
                    <td>
                      <div class="btn-group" role="group">
                        <button 
                          @click="viewReservationDetails(reservation)" 
                          class="btn btn-sm btn-outline-primary"
                          title="View Details"
                        >
                          <i class="fas fa-eye"></i>
                        </button>
                        
                        <!-- Start Parking (for reserved status) -->
                        <button
                          v-if="reservation.status === 'reserved'"
                          @click="updateReservationStatus(reservation, 'active')"
                          class="btn btn-sm btn-outline-success"
                          title="Start Parking"
                          :disabled="actionLoading === reservation.id"
                        >
                          <span v-if="actionLoading === reservation.id" class="spinner-border spinner-border-sm"></span>
                          <i v-else class="fas fa-play"></i>
                        </button>

                        <!-- End Parking (for active status) -->
                        <button
                          v-if="reservation.status === 'active'"
                          @click="updateReservationStatus(reservation, 'completed')"
                          class="btn btn-sm btn-outline-warning"
                          title="End Parking"
                          :disabled="actionLoading === reservation.id"
                        >
                          <span v-if="actionLoading === reservation.id" class="spinner-border spinner-border-sm"></span>
                          <i v-else class="fas fa-stop"></i>
                        </button>

                        <!-- Cancel Reservation -->
                        <button
                          v-if="['reserved', 'active'].includes(reservation.status)"
                          @click="cancelReservation(reservation)"
                          class="btn btn-sm btn-outline-danger"
                          title="Cancel"
                          :disabled="actionLoading === reservation.id"
                        >
                          <i class="fas fa-times"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          
          <!-- Pagination -->
          <div v-if="filteredReservations.length > itemsPerPage" class="card-footer">
            <nav>
              <ul class="pagination pagination-sm justify-content-center mb-0">
                <li class="page-item" :class="{ disabled: currentPage === 1 }">
                  <button @click="currentPage = Math.max(1, currentPage - 1)" class="page-link">Previous</button>
                </li>
                <li 
                  v-for="page in totalPages" 
                  :key="page"
                  class="page-item"
                  :class="{ active: currentPage === page }"
                >
                  <button @click="currentPage = page" class="page-link">{{ page }}</button>
                </li>
                <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                  <button @click="currentPage = Math.min(totalPages, currentPage + 1)" class="page-link">Next</button>
                </li>
              </ul>
            </nav>
          </div>
        </div>
      </div>
    </div>

    <!-- Reservation Details Modal -->
    <div class="modal fade" id="reservationDetailsModal" tabindex="-1">
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
                  <h6>Reservation Information</h6>
                  <table class="table table-sm">
                    <tr>
                      <td><strong>ID:</strong></td>
                      <td>#{{ selectedReservation.id }}</td>
                    </tr>
                    <tr>
                      <td><strong>Status:</strong></td>
                      <td>
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
                      </td>
                    </tr>
                    <tr>
                      <td><strong>Vehicle:</strong></td>
                      <td>{{ selectedReservation.vehicle_number || 'N/A' }}</td>
                    </tr>
                    <tr>
                      <td><strong>Duration:</strong></td>
                      <td>{{ selectedReservation.duration_hours || 0 }} hours</td>
                    </tr>
                    <tr>
                      <td><strong>Total Cost:</strong></td>
                      <td class="text-success fw-bold">${{ selectedReservation.parking_cost || 0 }}</td>
                    </tr>
                  </table>
                </div>
                
                <div class="col-md-6">
                  <h6>User Information</h6>
                  <table class="table table-sm">
                    <tr>
                      <td><strong>Name:</strong></td>
                      <td>{{ selectedReservation.user_name }}</td>
                    </tr>
                    <tr>
                      <td><strong>Email:</strong></td>
                      <td>{{ selectedReservation.user?.email || 'N/A' }}</td>
                    </tr>
                    <tr>
                      <td><strong>Phone:</strong></td>
                      <td>{{ selectedReservation.user?.phone_number || 'N/A' }}</td>
                    </tr>
                  </table>
                  
                  <h6 class="mt-3">Parking Information</h6>
                  <table class="table table-sm">
                    <tr>
                      <td><strong>Location:</strong></td>
                      <td>{{ selectedReservation.parking_lot_name }}</td>
                    </tr>
                    <tr>
                      <td><strong>Spot:</strong></td>
                      <td>{{ selectedReservation.spot_number }}</td>
                    </tr>
                    <tr>
                      <td><strong>Address:</strong></td>
                      <td>{{ selectedReservation.parking_lot?.address || 'N/A' }}</td>
                    </tr>
                  </table>
                </div>
              </div>
              
              <div class="row mb-3">
                <div class="col-12">
                  <h6>Timeline</h6>
                  <table class="table table-sm">
                    <tr>
                      <td><strong>Reserved At:</strong></td>
                      <td>{{ formatDateTime(selectedReservation.reservation_timestamp) }}</td>
                    </tr>
                    <tr v-if="selectedReservation.parking_timestamp">
                      <td><strong>Parked At:</strong></td>
                      <td>{{ formatDateTime(selectedReservation.parking_timestamp) }}</td>
                    </tr>
                    <tr v-if="selectedReservation.leaving_timestamp">
                      <td><strong>Left At:</strong></td>
                      <td>{{ formatDateTime(selectedReservation.leaving_timestamp) }}</td>
                    </tr>
                  </table>
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
            <div v-if="selectedReservation && ['reserved', 'active'].includes(selectedReservation.status)">
              <button 
                v-if="selectedReservation.status === 'reserved'"
                @click="updateReservationStatus(selectedReservation, 'active')"
                type="button" 
                class="btn btn-success me-2"
                :disabled="actionLoading === selectedReservation.id"
              >
                <span v-if="actionLoading === selectedReservation.id" class="spinner-border spinner-border-sm me-2"></span>
                Start Parking
              </button>
              <button 
                v-if="selectedReservation.status === 'active'"
                @click="updateReservationStatus(selectedReservation, 'completed')"
                type="button" 
                class="btn btn-warning me-2"
                :disabled="actionLoading === selectedReservation.id"
              >
                <span v-if="actionLoading === selectedReservation.id" class="spinner-border spinner-border-sm me-2"></span>
                End Parking
              </button>
              <button 
                @click="cancelReservation(selectedReservation)"
                type="button" 
                class="btn btn-danger"
                :disabled="actionLoading === selectedReservation.id"
              >
                Cancel Reservation
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'AdminReservations',
  data() {
    return {
      loading: false,
      actionLoading: null,
      searchQuery: '',
      statusFilter: '',
      dateFrom: '',
      dateTo: '',
      currentPage: 1,
      itemsPerPage: 15,
      reservations: [],
      selectedReservation: null,
      refreshInterval: null,
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
      
      // Filter by search query
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(reservation => 
          reservation.user_name?.toLowerCase().includes(query) ||
          reservation.parking_lot_name?.toLowerCase().includes(query) ||
          reservation.vehicle_number?.toLowerCase().includes(query) ||
          reservation.spot_number?.toLowerCase().includes(query)
        )
      }
      
      // Filter by status
      if (this.statusFilter) {
        filtered = filtered.filter(reservation => reservation.status === this.statusFilter)
      }
      
      // Filter by date range
      if (this.dateFrom) {
        filtered = filtered.filter(reservation => {
          const reservationDate = new Date(reservation.reservation_timestamp).toISOString().split('T')[0]
          return reservationDate >= this.dateFrom
        })
      }
      
      if (this.dateTo) {
        filtered = filtered.filter(reservation => {
          const reservationDate = new Date(reservation.reservation_timestamp).toISOString().split('T')[0]
          return reservationDate <= this.dateTo
        })
      }
      
      // Sort by creation date (newest first)
      return filtered.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    },
    
    totalPages() {
      return Math.ceil(this.filteredReservations.length / this.itemsPerPage)
    },
    
    paginatedReservations() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      return this.filteredReservations.slice(start, start + this.itemsPerPage)
    }
  },
  async mounted() {
    await this.loadReservations()
    
    // Check for user_id query parameter
    if (this.$route.query.user_id) {
      this.searchQuery = this.$route.query.user_id
    }
    
    // Set up auto-refresh every 30 seconds
    this.refreshInterval = setInterval(() => {
      if (!this.loading) {
        this.loadReservations()
      }
    }, 30000)
  },
  
  beforeUnmount() {
    // Clear the refresh interval when component is destroyed
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval)
    }
  },
  methods: {
    ...mapActions('admin', ['fetchReservations', 'updateReservationStatus', 'cancelReservation']),
    
    async loadReservations() {
      this.loading = true
      try {
        const result = await this.fetchReservations({ page: 1, perPage: 1000 })
        this.reservations = result.reservations
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
    
    viewReservationDetails(reservation) {
      this.selectedReservation = reservation
      const modal = new window.bootstrap.Modal(document.getElementById('reservationDetailsModal'))
      modal.show()
    },
    
    async updateReservationStatus(reservation, newStatus) {
      this.actionLoading = reservation.id
      try {
        const updateData = {
          id: reservation.id,
          status: newStatus
        }
        
        if (newStatus === 'active') {
          updateData.parking_timestamp = new Date().toISOString()
        } else if (newStatus === 'completed') {
          updateData.leaving_timestamp = new Date().toISOString()
        }
        
        await this.updateReservationStatus(updateData)
        await this.loadReservations()
        
        // Update selected reservation if modal is open
        if (this.selectedReservation && this.selectedReservation.id === reservation.id) {
          this.selectedReservation = this.reservations.find(r => r.id === reservation.id)
        }
        
        this.$toast?.success(`Reservation ${newStatus} successfully!`)
        
      } catch (error) {
        console.error('Error updating reservation status:', error)
        this.$toast?.error('Failed to update reservation status')
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
        await this.cancelReservation(reservation.id)
        await this.loadReservations()
        
        // Update selected reservation if modal is open
        if (this.selectedReservation && this.selectedReservation.id === reservation.id) {
          this.selectedReservation = this.reservations.find(r => r.id === reservation.id)
        }
        
        this.$toast?.success('Reservation cancelled successfully!')
        
      } catch (error) {
        console.error('Error cancelling reservation:', error)
        this.$toast?.error('Failed to cancel reservation')
      } finally {
        this.actionLoading = null
      }
    },
    
    exportReservations() {
      // Create CSV content
      const headers = ['ID', 'User', 'Parking Lot', 'Spot', 'Vehicle', 'Reserved At', 'Status', 'Duration (h)', 'Cost']
      const csvContent = [
        headers.join(','),
        ...this.filteredReservations.map(reservation => [
          reservation.id,
          `"${reservation.user_name || 'N/A'}"`,
          `"${reservation.parking_lot_name || 'N/A'}"`,
          reservation.spot_number || 'N/A',
          reservation.vehicle_number || 'N/A',
          this.formatDateTime(reservation.reservation_timestamp),
          reservation.status,
          reservation.duration_hours || 0,
          reservation.parking_cost || 0
        ].join(','))
      ].join('\n')
      
      // Download CSV
      const blob = new Blob([csvContent], { type: 'text/csv' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `reservations_export_${new Date().toISOString().split('T')[0]}.csv`
      a.click()
      window.URL.revokeObjectURL(url)
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
    
    formatDate(dateString) {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleDateString()
    },
    
    formatTime(dateString) {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleTimeString()
    },
    
    formatDateTime(dateString) {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleString()
    }
  }
}
</script>

<style scoped>
.stats-card {
  border: none;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  border-radius: 12px;
  transition: transform 0.2s;
}

.stats-card:hover {
  transform: translateY(-2px);
}

.card {
  border-radius: 12px;
  border: none;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.table th {
  border-top: none;
  font-weight: 600;
  background-color: #f8f9fa;
}

.btn {
  border-radius: 8px;
}

.btn-group .btn {
  border-radius: 0;
}

.btn-group .btn:first-child {
  border-radius: 8px 0 0 8px;
}

.btn-group .btn:last-child {
  border-radius: 0 8px 8px 0;
}

.modal-content {
  border-radius: 12px;
  border: none;
}

.pagination .page-link {
  border-radius: 8px;
  margin: 0 2px;
  border: none;
  background-color: #f8f9fa;
}

.pagination .page-item.active .page-link {
  background-color: #007bff;
  border-color: #007bff;
}

.badge {
  font-size: 0.75rem;
  padding: 0.5em 0.75em;
}
</style>
