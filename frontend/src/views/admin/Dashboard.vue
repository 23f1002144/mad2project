<template>
  <div class="container-fluid mt-4">
    <!-- Welcome Header -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="card bg-gradient-primary text-white">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h2 class="card-title mb-1">Admin Dashboard</h2>
                <p class="card-text mb-0">Monitor and manage the parking system</p>
              </div>
              <div class="text-end">
                <h5 class="mb-0">{{ currentDateTime }}</h5>
                <small>Last updated: {{ lastRefresh }}</small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Stats -->
    <div class="row mb-4">
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="card text-center stats-card border-start border-4 border-primary">
          <div class="card-body">
            <i class="fas fa-building fa-2x text-primary mb-2"></i>
            <h3 class="mb-1">{{ stats.totalLots }}</h3>
            <p class="text-muted mb-0">Total Parking Lots</p>
            <small class="text-success">{{ stats.activeLots }} active</small>
          </div>
        </div>
      </div>
      
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="card text-center stats-card border-start border-4 border-success">
          <div class="card-body">
            <i class="fas fa-car fa-2x text-success mb-2"></i>
            <h3 class="mb-1">{{ stats.totalSpots }}</h3>
            <p class="text-muted mb-0">Total Parking Spots</p>
            <small class="text-warning">{{ stats.availableSpots }} available</small>
          </div>
        </div>
      </div>
      
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="card text-center stats-card border-start border-4 border-info">
          <div class="card-body">
            <i class="fas fa-users fa-2x text-info mb-2"></i>
            <h3 class="mb-1">{{ stats.totalUsers }}</h3>
            <p class="text-muted mb-0">Registered Users</p>
            <small class="text-success">{{ stats.activeUsers }} active</small>
          </div>
        </div>
      </div>
      
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="card text-center stats-card border-start border-4 border-warning">
          <div class="card-body">
            <i class="fas fa-calendar-check fa-2x text-warning mb-2"></i>
            <h3 class="mb-1">{{ stats.totalReservations }}</h3>
            <p class="text-muted mb-0">Total Reservations</p>
            <small class="text-info">{{ stats.activeReservations }} active</small>
          </div>
        </div>
      </div>
    </div>

    <!-- Revenue and Occupancy Charts -->
    <div class="row mb-4">
      <div class="col-lg-8 mb-3">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">Revenue Overview</h5>
          </div>
          <div class="card-body">
            <div class="row text-center mb-3">
              <div class="col-md-4">
                <div class="revenue-stat">
                  <h4 class="text-success">${{ stats.todayRevenue }}</h4>
                  <small class="text-muted">Today</small>
                </div>
              </div>
              <div class="col-md-4">
                <div class="revenue-stat">
                  <h4 class="text-info">${{ stats.weekRevenue }}</h4>
                  <small class="text-muted">This Week</small>
                </div>
              </div>
              <div class="col-md-4">
                <div class="revenue-stat">
                  <h4 class="text-warning">${{ stats.monthRevenue }}</h4>
                  <small class="text-muted">This Month</small>
                </div>
              </div>
            </div>
            <!-- Placeholder for chart -->
            <div class="chart-placeholder">
              <i class="fas fa-chart-line fa-3x text-muted"></i>
              <p class="text-muted mt-2">Revenue chart visualization would go here</p>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-4 mb-3">
        <div class="card h-100">
          <div class="card-header">
            <h5 class="mb-0">Occupancy Rate</h5>
          </div>
          <div class="card-body d-flex flex-column justify-content-center">
            <div class="text-center">
              <div class="occupancy-circle">
                <span class="occupancy-percentage">{{ occupancyRate }}%</span>
              </div>
              <p class="mt-3 mb-2">Overall Occupancy</p>
              <div class="progress">
                <div 
                  class="progress-bar"
                  :class="{
                    'bg-success': occupancyRate < 50,
                    'bg-warning': occupancyRate >= 50 && occupancyRate < 80,
                    'bg-danger': occupancyRate >= 80
                  }"
                  :style="{ width: occupancyRate + '%' }"
                ></div>
              </div>
            </div>
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
              <div class="col-lg-3 col-md-6 mb-3">
                <router-link to="/admin/lots" class="btn btn-outline-primary w-100 h-100 d-flex flex-column justify-content-center">
                  <i class="fas fa-building fa-2x mb-2"></i>
                  Manage Parking Lots
                </router-link>
              </div>
              <div class="col-lg-3 col-md-6 mb-3">
                <router-link to="/admin/users" class="btn btn-outline-success w-100 h-100 d-flex flex-column justify-content-center">
                  <i class="fas fa-users fa-2x mb-2"></i>
                  Manage Users
                </router-link>
              </div>
              <div class="col-lg-3 col-md-6 mb-3">
                <router-link to="/admin/reservations" class="btn btn-outline-info w-100 h-100 d-flex flex-column justify-content-center">
                  <i class="fas fa-calendar-alt fa-2x mb-2"></i>
                  View Reservations
                </router-link>
              </div>
              <div class="col-lg-3 col-md-6 mb-3">
                <button @click="refreshDashboard" class="btn btn-outline-secondary w-100 h-100 d-flex flex-column justify-content-center" :disabled="loading">
                  <i class="fas fa-sync-alt fa-2x mb-2" :class="{ 'fa-spin': loading }"></i>
                  Refresh Data
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="row mb-4">
      <div class="col-lg-6 mb-3">
        <div class="card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="mb-0">Recent Reservations</h5>
            <router-link to="/admin/reservations" class="btn btn-sm btn-outline-primary">View All</router-link>
          </div>
          <div class="card-body">
            <div v-if="loading" class="text-center py-3">
              <div class="spinner-border spinner-border-sm"></div>
            </div>
            <div v-else-if="recentReservations.length === 0" class="text-center py-3 text-muted">
              No recent reservations
            </div>
            <div v-else>
              <div v-for="reservation in recentReservations" :key="reservation.id" class="d-flex justify-content-between align-items-center mb-2 pb-2 border-bottom">
                <div>
                  <div class="fw-bold">{{ reservation.user_name }}</div>
                  <small class="text-muted">{{ reservation.parking_lot_name }} - Spot {{ reservation.spot_number }}</small>
                </div>
                <div class="text-end">
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
                  <div><small class="text-muted">{{ formatTime(reservation.created_at) }}</small></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-6 mb-3">
        <div class="card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="mb-0">System Alerts</h5>
            <span class="badge bg-danger">{{ alerts.length }}</span>
          </div>
          <div class="card-body">
            <div v-if="alerts.length === 0" class="text-center py-3 text-muted">
              <i class="fas fa-check-circle fa-2x text-success"></i>
              <p class="mt-2 mb-0">All systems running smoothly</p>
            </div>
            <div v-else>
              <div v-for="alert in alerts" :key="alert.id" class="alert alert-warning alert-sm mb-2">
                <i class="fas fa-exclamation-triangle me-2"></i>
                {{ alert.message }}
              </div>
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
  name: 'AdminDashboard',
  data() {
    return {
      loading: false,
      currentDateTime: '',
      lastRefresh: '',
      stats: {
        totalLots: 0,
        activeLots: 0,
        totalSpots: 0,
        availableSpots: 0,
        totalUsers: 0,
        activeUsers: 0,
        totalReservations: 0,
        activeReservations: 0,
        todayRevenue: 0,
        weekRevenue: 0,
        monthRevenue: 0
      },
      recentReservations: [],
      alerts: []
    }
  },
  computed: {
    occupancyRate() {
      if (this.stats.totalSpots === 0) return 0
      const occupiedSpots = this.stats.totalSpots - this.stats.availableSpots
      return Math.round((occupiedSpots / this.stats.totalSpots) * 100)
    }
  },
  async mounted() {
    this.startClock()
    await this.loadDashboardData()
  },
  beforeUnmount() {
    if (this.clockInterval) {
      clearInterval(this.clockInterval)
    }
  },
  methods: {
    ...mapActions('admin', ['fetchDashboardStats', 'fetchRecentReservations']),
    
    startClock() {
      this.updateDateTime()
      this.clockInterval = setInterval(this.updateDateTime, 1000)
    },
    
    updateDateTime() {
      this.currentDateTime = new Date().toLocaleString()
    },
    
    async loadDashboardData() {
      this.loading = true
      try {
        await Promise.all([
          this.loadStats(),
          this.loadRecentReservations(),
          this.checkSystemAlerts()
        ])
        this.lastRefresh = new Date().toLocaleTimeString()
      } catch (error) {
        console.error('Error loading dashboard data:', error)
      } finally {
        this.loading = false
      }
    },
    
    async loadStats() {
      try {
        const dashboardStats = await this.fetchDashboardStats()
        this.stats = { ...this.stats, ...dashboardStats }
      } catch (error) {
        console.error('Error loading stats:', error)
      }
    },
    
    async loadRecentReservations() {
      try {
        const reservations = await this.fetchRecentReservations()
        this.recentReservations = reservations.slice(0, 5) // Show only 5 recent
      } catch (error) {
        console.error('Error loading recent reservations:', error)
      }
    },
    
    async checkSystemAlerts() {
      // Generate system alerts based on data
      this.alerts = []
      
      // Check for low availability
      if (this.occupancyRate > 90) {
        this.alerts.push({
          id: 1,
          message: 'High occupancy rate detected - consider adding more parking lots'
        })
      }
      
      // Check for inactive lots
      if (this.stats.totalLots > this.stats.activeLots) {
        const inactiveLots = this.stats.totalLots - this.stats.activeLots
        this.alerts.push({
          id: 2,
          message: `${inactiveLots} parking lot(s) are currently inactive`
        })
      }
      
      // Check for pending reservations
      if (this.stats.activeReservations > this.stats.availableSpots) {
        this.alerts.push({
          id: 3,
          message: 'More active reservations than available spots - review reservations'
        })
      }
    },
    
    async refreshDashboard() {
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
    
    formatTime(dateString) {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleTimeString()
    }
  }
}
</script>

<style scoped>
.bg-gradient-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stats-card {
  border: none;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  border-radius: 12px;
  transition: transform 0.2s;
}

.stats-card:hover {
  transform: translateY(-4px);
}

.card {
  border-radius: 12px;
  border: none;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.revenue-stat {
  padding: 1rem;
  border-radius: 8px;
  background-color: #f8f9fa;
}

.chart-placeholder {
  text-align: center;
  padding: 3rem;
  background-color: #f8f9fa;
  border-radius: 8px;
  margin-top: 1rem;
}

.occupancy-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: conic-gradient(
    #28a745 0deg,
    #28a745 calc(var(--percentage, 0) * 3.6deg),
    #e9ecef calc(var(--percentage, 0) * 3.6deg),
    #e9ecef 360deg
  );
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  position: relative;
}

.occupancy-circle::before {
  content: '';
  width: 90px;
  height: 90px;
  border-radius: 50%;
  background: white;
  position: absolute;
}

.occupancy-percentage {
  font-size: 1.5rem;
  font-weight: bold;
  z-index: 1;
  position: relative;
}

.btn {
  border-radius: 8px;
  font-weight: 500;
  min-height: 120px;
}

.alert-sm {
  padding: 0.5rem;
  font-size: 0.9rem;
}

.border-start {
  border-left-width: 4px !important;
}

.fa-spin {
  animation: fa-spin 1s infinite linear;
}

@keyframes fa-spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
