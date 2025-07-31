<template>
  <div class="container-fluid mt-4">
    <!-- Alert Messages -->
    <div v-if="$store.state.alert.message" class="row mb-4">
      <div class="col-12">
        <div :class="`alert alert-${$store.state.alert.type} alert-dismissible fade show`" role="alert">
          {{ $store.state.alert.message }}
          <button type="button" class="btn-close" @click="$store.dispatch('clearAlert')"></button>
        </div>
      </div>
    </div>

    <!-- Page Header -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center">
          <h2>Manage Users</h2>
          <div class="d-flex gap-2">
            <button @click="refreshUsers" class="btn btn-outline-primary" :disabled="loading">
              <i class="fas fa-sync-alt me-2" :class="{ 'fa-spin': loading }"></i>
              Refresh
            </button>
            <button @click="exportUsers" class="btn btn-outline-success">
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
              <div class="col-md-4 mb-3">
                <label for="search" class="form-label">Search Users</label>
                <input
                  type="text"
                  class="form-control"
                  id="search"
                  v-model="searchQuery"
                  placeholder="Search by name, username, or email..."
                />
              </div>
              <div class="col-md-4 mb-3">
                <label for="statusFilter" class="form-label">Status</label>
                <select class="form-select" id="statusFilter" v-model="statusFilter">
                  <option value="">All Users</option>
                  <option value="active">Active</option>
                  <option value="inactive">Inactive</option>
                </select>
              </div>
              <div class="col-md-4 mb-3">
                <label for="sortBy" class="form-label">Sort By</label>
                <select class="form-select" id="sortBy" v-model="sortBy">
                  <option value="name">Name</option>
                  <option value="email">Email</option>
                  <option value="created_at">Join Date</option>
                  <option value="reservations">Reservations Count</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- User Statistics -->
    <div class="row mb-4">
      <div class="col-md-3 col-sm-6 mb-3">
        <div class="card text-center stats-card bg-primary text-white">
          <div class="card-body">
            <i class="fas fa-users fa-2x mb-2"></i>
            <h3 class="mb-1">{{ stats.totalUsers }}</h3>
            <p class="mb-0">Total Users</p>
          </div>
        </div>
      </div>
      
      <div class="col-md-3 col-sm-6 mb-3">
        <div class="card text-center stats-card bg-success text-white">
          <div class="card-body">
            <i class="fas fa-user-check fa-2x mb-2"></i>
            <h3 class="mb-1">{{ stats.activeUsers }}</h3>
            <p class="mb-0">Active Users</p>
          </div>
        </div>
      </div>
      
      <div class="col-md-3 col-sm-6 mb-3">
        <div class="card text-center stats-card bg-info text-white">
          <div class="card-body">
            <i class="fas fa-calendar-check fa-2x mb-2"></i>
            <h3 class="mb-1">{{ stats.usersWithReservations }}</h3>
            <p class="mb-0">Users with Reservations</p>
          </div>
        </div>
      </div>
      
      <div class="col-md-3 col-sm-6 mb-3">
        <div class="card text-center stats-card bg-warning text-dark">
          <div class="card-body">
            <i class="fas fa-user-plus fa-2x mb-2"></i>
            <h3 class="mb-1">{{ stats.newUsersThisMonth }}</h3>
            <p class="mb-0">New This Month</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3 text-muted">Loading users...</p>
    </div>

    <!-- Users Table -->
    <div v-else class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">Users ({{ filteredUsers.length }})</h5>
          </div>
          <div class="card-body p-0">
            <div v-if="filteredUsers.length === 0" class="text-center py-5">
              <i class="fas fa-users fa-3x text-muted mb-3"></i>
              <h5 class="text-muted">No users found</h5>
              <p class="text-muted">Try adjusting your search criteria.</p>
            </div>
            <div v-else class="table-responsive">
              <table class="table table-hover mb-0">
                <thead class="bg-light">
                  <tr>
                    <th>User</th>
                    <th>Contact</th>
                    <th>Join Date</th>
                    <th>Reservations</th>
                    <th>Total Spent</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="user in paginatedUsers" :key="user.id">
                    <td>
                      <div class="d-flex align-items-center">
                        <div class="user-avatar me-3">
                          <i class="fas fa-user"></i>
                        </div>
                        <div>
                          <div class="fw-bold">{{ user.first_name }} {{ user.last_name }}</div>
                          <small class="text-muted">@{{ user.username }}</small>
                        </div>
                      </div>
                    </td>
                    <td>
                      <div>{{ user.email }}</div>
                      <small class="text-muted">{{ user.phone_number || 'No phone' }}</small>
                    </td>
                    <td>
                      <div>{{ formatDate(user.created_at) }}</div>
                      <small class="text-muted">{{ getRelativeTime(user.created_at) }}</small>
                    </td>
                    <td class="text-center">
                      <span class="badge bg-info">{{ user.reservations_count || 0 }}</span>
                    </td>
                    <td class="text-center">
                      <span class="fw-bold text-success">${{ user.total_spent || 0 }}</span>
                    </td>
                    <td>
                      <span 
                        class="badge"
                        :class="user.is_active ? 'bg-success' : 'bg-secondary'"
                      >
                        {{ user.is_active ? 'Active' : 'Inactive' }}
                      </span>
                    </td>
                    <td>
                      <div class="btn-group" role="group">
                        <button 
                          @click="viewUserDetails(user)" 
                          class="btn btn-sm btn-outline-primary"
                          title="View Details"
                        >
                          <i class="fas fa-eye"></i>
                        </button>
                        <button 
                          @click="viewUserReservations(user)" 
                          class="btn btn-sm btn-outline-info"
                          title="View Reservations"
                        >
                          <i class="fas fa-calendar"></i>
                        </button>
                        <button 
                          @click="toggleUserStatus(user)" 
                          class="btn btn-sm"
                          :class="user.is_active ? 'btn-outline-warning' : 'btn-outline-success'"
                          :title="user.is_active ? 'Deactivate' : 'Activate'"
                          :disabled="actionLoading === user.id"
                        >
                          <span v-if="actionLoading === user.id" class="spinner-border spinner-border-sm"></span>
                          <i v-else class="fas" :class="user.is_active ? 'fa-user-slash' : 'fa-user-check'"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          
          <!-- Pagination -->
          <div v-if="filteredUsers.length > itemsPerPage" class="card-footer">
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

    <!-- User Details Modal -->
    <div class="modal fade" id="userDetailsModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">User Details</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div v-if="selectedUser">
              <div class="row">
                <div class="col-md-6 mb-4">
                  <h6>Personal Information</h6>
                  <table class="table table-sm">
                    <tr>
                      <td><strong>Name:</strong></td>
                      <td>{{ selectedUser.first_name }} {{ selectedUser.last_name }}</td>
                    </tr>
                    <tr>
                      <td><strong>Username:</strong></td>
                      <td>@{{ selectedUser.username }}</td>
                    </tr>
                    <tr>
                      <td><strong>Email:</strong></td>
                      <td>{{ selectedUser.email }}</td>
                    </tr>
                    <tr>
                      <td><strong>Phone:</strong></td>
                      <td>{{ selectedUser.phone_number || 'Not provided' }}</td>
                    </tr>
                    <tr>
                      <td><strong>Status:</strong></td>
                      <td>
                        <span 
                          class="badge"
                          :class="selectedUser.is_active ? 'bg-success' : 'bg-secondary'"
                        >
                          {{ selectedUser.is_active ? 'Active' : 'Inactive' }}
                        </span>
                      </td>
                    </tr>
                  </table>
                </div>
                
                <div class="col-md-6 mb-4">
                  <h6>Account Information</h6>
                  <table class="table table-sm">
                    <tr>
                      <td><strong>User ID:</strong></td>
                      <td>#{{ selectedUser.id }}</td>
                    </tr>
                    <tr>
                      <td><strong>Joined:</strong></td>
                      <td>{{ formatDate(selectedUser.created_at) }}</td>
                    </tr>
                    <tr>
                      <td><strong>Last Updated:</strong></td>
                      <td>{{ formatDate(selectedUser.updated_at) }}</td>
                    </tr>
                    <tr>
                      <td><strong>Total Reservations:</strong></td>
                      <td>{{ selectedUser.reservations_count || 0 }}</td>
                    </tr>
                    <tr>
                      <td><strong>Total Spent:</strong></td>
                      <td class="text-success fw-bold">${{ selectedUser.total_spent || 0 }}</td>
                    </tr>
                  </table>
                </div>
              </div>
              
              <div v-if="userReservations.length > 0">
                <h6>Recent Reservations</h6>
                <div class="table-responsive">
                  <table class="table table-sm">
                    <thead>
                      <tr>
                        <th>Parking Lot</th>
                        <th>Spot</th>
                        <th>Date</th>
                        <th>Status</th>
                        <th>Cost</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="reservation in userReservations.slice(0, 5)" :key="reservation.id">
                        <td>{{ reservation.parking_lot_name }}</td>
                        <td>{{ reservation.spot_number }}</td>
                        <td>{{ formatDate(reservation.reservation_timestamp) }}</td>
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
                        <td>${{ reservation.parking_cost || 0 }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button 
              v-if="selectedUser"
              @click="toggleUserStatus(selectedUser)"
              type="button" 
              class="btn"
              :class="selectedUser.is_active ? 'btn-warning' : 'btn-success'"
              :disabled="actionLoading === selectedUser.id"
            >
              <span v-if="actionLoading === selectedUser.id" class="spinner-border spinner-border-sm me-2"></span>
              {{ selectedUser.is_active ? 'Deactivate User' : 'Activate User' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'AdminUsers',
  data() {
    return {
      loading: false,
      actionLoading: null,
      searchQuery: '',
      statusFilter: '',
      sortBy: 'name',
      currentPage: 1,
      itemsPerPage: 10,
      users: [],
      selectedUser: null,
      userReservations: [],
      stats: {
        totalUsers: 0,
        activeUsers: 0,
        usersWithReservations: 0,
        newUsersThisMonth: 0
      }
    }
  },
  computed: {
    filteredUsers() {
      let filtered = this.users
      
      // Filter by search query
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(user => 
          user.first_name.toLowerCase().includes(query) ||
          user.last_name.toLowerCase().includes(query) ||
          user.username.toLowerCase().includes(query) ||
          user.email.toLowerCase().includes(query)
        )
      }
      
      // Filter by status
      if (this.statusFilter) {
        const isActive = this.statusFilter === 'active'
        filtered = filtered.filter(user => user.is_active === isActive)
      }
      
      // Sort results
      return filtered.sort((a, b) => {
        switch (this.sortBy) {
          case 'email':
            return a.email.localeCompare(b.email)
          case 'created_at':
            return new Date(b.created_at) - new Date(a.created_at)
          case 'reservations':
            return (b.reservations_count || 0) - (a.reservations_count || 0)
          default:
            return `${a.first_name} ${a.last_name}`.localeCompare(`${b.first_name} ${b.last_name}`)
        }
      })
    },
    
    totalPages() {
      return Math.ceil(this.filteredUsers.length / this.itemsPerPage)
    },
    
    paginatedUsers() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      return this.filteredUsers.slice(start, start + this.itemsPerPage)
    }
  },
  async mounted() {
    await this.loadUsers()
  },
  methods: {
    ...mapActions('admin', ['fetchAllUsers', 'updateUserStatus', 'fetchUserReservations']),
    
    async loadUsers() {
      this.loading = true
      try {
        this.users = await this.fetchAllUsers()
        this.calculateStats()
      } catch (error) {
        console.error('Error loading users:', error)
        // Error alert is handled by the store action
      } finally {
        this.loading = false
      }
    },
    
    calculateStats() {
      const now = new Date()
      const thisMonth = new Date(now.getFullYear(), now.getMonth(), 1)
      
      this.stats = {
        totalUsers: this.users.length,
        activeUsers: this.users.filter(u => u.is_active).length,
        usersWithReservations: this.users.filter(u => (u.reservations_count || 0) > 0).length,
        newUsersThisMonth: this.users.filter(u => new Date(u.created_at) >= thisMonth).length
      }
    },
    
    async refreshUsers() {
      await this.loadUsers()
    },
    
    async viewUserDetails(user) {
      this.selectedUser = user
      this.userReservations = []
      
      const modal = new window.bootstrap.Modal(document.getElementById('userDetailsModal'))
      modal.show()
      
      try {
        this.userReservations = await this.fetchUserReservations(user.id)
      } catch (error) {
        console.error('Error loading user reservations:', error)
      }
    },
    
    viewUserReservations(user) {
      // This could navigate to a detailed reservations view
      this.$router.push({
        name: 'AdminReservations',
        query: { user_id: user.id }
      })
    },
    
    async toggleUserStatus(user) {
      this.actionLoading = user.id
      try {
        await this.updateUserStatus({
          id: user.id,
          is_active: !user.is_active
        })
        
        await this.loadUsers()
        
        // Update selected user if modal is open
        if (this.selectedUser && this.selectedUser.id === user.id) {
          this.selectedUser = this.users.find(u => u.id === user.id)
        }
        
      } catch (error) {
        console.error('Error toggling user status:', error)
        // Error alert is handled by the store action
      } finally {
        this.actionLoading = null
      }
    },
    
    exportUsers() {
      // Create CSV content
      const headers = ['ID', 'First Name', 'Last Name', 'Username', 'Email', 'Phone', 'Status', 'Join Date', 'Reservations', 'Total Spent']
      const csvContent = [
        headers.join(','),
        ...this.filteredUsers.map(user => [
          user.id,
          `"${user.first_name}"`,
          `"${user.last_name}"`,
          user.username,
          user.email,
          user.phone_number || '',
          user.is_active ? 'Active' : 'Inactive',
          this.formatDate(user.created_at),
          user.reservations_count || 0,
          user.total_spent || 0
        ].join(','))
      ].join('\n')
      
      // Download CSV
      const blob = new Blob([csvContent], { type: 'text/csv' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `users_export_${new Date().toISOString().split('T')[0]}.csv`
      a.click()
      window.URL.revokeObjectURL(url)
    },
    
    formatDate(dateString) {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleDateString()
    },
    
    getRelativeTime(dateString) {
      if (!dateString) return 'N/A'
      const now = new Date()
      const date = new Date(dateString)
      const diffTime = Math.abs(now - date)
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      
      if (diffDays < 7) return `${diffDays} days ago`
      if (diffDays < 30) return `${Math.ceil(diffDays / 7)} weeks ago`
      if (diffDays < 365) return `${Math.ceil(diffDays / 30)} months ago`
      return `${Math.ceil(diffDays / 365)} years ago`
    },
    
    formatStatus(status) {
      const statusMap = {
        'reserved': 'Reserved',
        'active': 'Active',
        'completed': 'Completed',
        'cancelled': 'Cancelled'
      }
      return statusMap[status] || status
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

.user-avatar {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
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
</style>
