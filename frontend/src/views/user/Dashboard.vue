<template>
  <div class="container-fluid mt-4">
    <!-- Welcome Header -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="card bg-primary text-white">
          <div class="card-body">
            <h2 class="card-title mb-1">Welcome, {{ userFullName }}!</h2>
            <p class="card-text mb-0">Manage your parking reservations from your dashboard</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Stats -->
    <div class="row mb-4">
      <div class="col-md-3 col-sm-6 mb-3">
        <div class="card text-center h-100">
          <div class="card-body">
            <i class="fas fa-calendar-check fa-2x text-success mb-2"></i>
            <h5 class="card-title">{{ stats.activeReservations }}</h5>
            <p class="card-text text-muted">Active Reservations</p>
          </div>
        </div>
      </div>
      
      <div class="col-md-3 col-sm-6 mb-3">
        <div class="card text-center h-100">
          <div class="card-body">
            <i class="fas fa-history fa-2x text-info mb-2"></i>
            <h5 class="card-title">{{ stats.totalReservations }}</h5>
            <p class="card-text text-muted">Total Reservations</p>
          </div>
        </div>
      </div>
      
      <div class="col-md-3 col-sm-6 mb-3">
        <div class="card text-center h-100">
          <div class="card-body">
            <i class="fas fa-dollar-sign fa-2x text-warning mb-2"></i>
            <h5 class="card-title">${{ stats.totalSpent }}</h5>
            <p class="card-text text-muted">Total Spent</p>
          </div>
        </div>
      </div>
      
      <div class="col-md-3 col-sm-6 mb-3">
        <div class="card text-center h-100">
          <div class="card-body">
            <i class="fas fa-parking fa-2x text-primary mb-2"></i>
            <h5 class="card-title">{{ stats.availableLots }}</h5>
            <p class="card-text text-muted">Available Lots</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">Quick Actions</h5>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-6 col-lg-3 mb-3">
                <router-link to="/parking-lots" class="btn btn-outline-primary w-100">
                  <i class="fas fa-search me-2"></i>Find Parking
                </router-link>
              </div>
              <div class="col-md-6 col-lg-3 mb-3">
                <router-link to="/reservations" class="btn btn-outline-success w-100">
                  <i class="fas fa-list me-2"></i>My Reservations
                </router-link>
              </div>
              <div class="col-md-6 col-lg-3 mb-3">
                <router-link to="/profile" class="btn btn-outline-info w-100">
                  <i class="fas fa-user me-2"></i>My Profile
                </router-link>
              </div>
              <div class="col-md-6 col-lg-3 mb-3">
                <button @click="refreshData" class="btn btn-outline-secondary w-100" :disabled="loading">
                  <i class="fas fa-sync-alt me-2" :class="{ 'fa-spin': loading }"></i>Refresh
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Reservations -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="mb-0">Recent Reservations</h5>
            <router-link to="/reservations" class="btn btn-sm btn-outline-primary">
              View All
            </router-link>
          </div>
          <div class="card-body">
            <div v-if="loading" class="text-center py-4">
              <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>
            
            <div v-else-if="recentReservations.length === 0" class="text-center py-4 text-muted">
              <i class="fas fa-calendar-times fa-3x mb-3"></i>
              <p>No reservations found. <router-link to="/parking-lots">Book your first parking spot!</router-link></p>
            </div>
            
            <div v-else class="table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>Parking Lot</th>
                    <th>Spot</th>
                    <th>Status</th>
                    <th>Date</th>
                    <th>Duration</th>
                    <th>Cost</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="reservation in recentReservations" :key="reservation.id">
                    <td>{{ reservation.parking_lot_name }}</td>
                    <td>{{ reservation.spot_number }}</td>
                    <td>
                      <span 
                        class="badge"
                        :class="{
                          'bg-warning': reservation.status === 'reserved',
                          'bg-success': reservation.status === 'active',
                          'bg-secondary': reservation.status === 'completed',
                          'bg-danger': reservation.status === 'cancelled'
                        }"
                      >
                        {{ formatStatus(reservation.status) }}
                      </span>
                    </td>
                    <td>{{ formatDate(reservation.reservation_timestamp) }}</td>
                    <td>{{ reservation.duration_hours || 0 }}h</td>
                    <td>${{ reservation.parking_cost || 0 }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'UserDashboard',
  data() {
    return {
      loading: false,
      stats: {
        activeReservations: 0,
        totalReservations: 0,
        totalSpent: 0,
        availableLots: 0
      },
      recentReservations: []
    }
  },
  computed: {
    ...mapGetters('auth', ['user']),
    userFullName() {
      return this.user ? `${this.user.first_name} ${this.user.last_name}` : 'User'
    }
  },
  async mounted() {
    await this.loadDashboardData()
  },
  methods: {
    ...mapActions('parking', ['fetchParkingLots']),
    ...mapActions('reservations', ['fetchUserReservations']),
    
    async loadDashboardData() {
      this.loading = true
      try {
        await Promise.all([
          this.loadStats(),
          this.loadRecentReservations()
        ])
      } catch (error) {
        console.error('Error loading dashboard data:', error)
      } finally {
        this.loading = false
      }
    },
    
    async loadStats() {
      try {
        // Fetch user reservations to calculate stats
        const reservations = await this.fetchUserReservations()
        
        this.stats.totalReservations = reservations.length
        this.stats.activeReservations = reservations.filter(r => 
          ['reserved', 'active'].includes(r.status)
        ).length
        this.stats.totalSpent = reservations
          .filter(r => r.parking_cost)
          .reduce((sum, r) => sum + parseFloat(r.parking_cost), 0)
          .toFixed(2)
        
        // Fetch parking lots to get available count
        const lots = await this.fetchParkingLots()
        this.stats.availableLots = lots.filter(lot => lot.is_active && lot.available_spots > 0).length
        
      } catch (error) {
        console.error('Error loading stats:', error)
      }
    },
    
    async loadRecentReservations() {
      try {
        const reservations = await this.fetchUserReservations()
        // Get the 5 most recent reservations
        this.recentReservations = reservations
          .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
          .slice(0, 5)
      } catch (error) {
        console.error('Error loading recent reservations:', error)
      }
    },
    
    async refreshData() {
      await this.loadDashboardData()
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
    }
  }
}
</script>

<style scoped>
.card {
  border-radius: 10px;
  border: none;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.card-body {
  padding: 1.5rem;
}

.btn {
  border-radius: 8px;
}

.table th {
  border-top: none;
  background-color: #f8f9fa;
  font-weight: 600;
}

.table-hover tbody tr:hover {
  background-color: rgba(0,0,0,0.02);
}

.bg-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
}

.fa-spin {
  animation: fa-spin 1s infinite linear;
}

@keyframes fa-spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
