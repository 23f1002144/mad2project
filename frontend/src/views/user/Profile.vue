<template>
  <div class="container mt-4">
    <div class="row justify-content-center">
      <div class="col-lg-8">
        <!-- Profile Header -->
        <div class="card mb-4">
          <div class="card-body text-center">
            <div class="avatar-placeholder mb-3">
              <i class="fas fa-user fa-3x text-primary"></i>
            </div>
            <h3 class="mb-1">{{ userFullName }}</h3>
            <p class="text-muted mb-0">{{ user?.email }}</p>
            <small class="text-muted">Member since {{ formatDate(user?.created_at) }}</small>
          </div>
        </div>

        <!-- Profile Form -->
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">Profile Information</h5>
          </div>
          <div class="card-body">
            <form @submit.prevent="updateProfile">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="firstName" class="form-label">First Name</label>
                  <input
                    type="text"
                    class="form-control"
                    id="firstName"
                    v-model="form.firstName"
                    required
                  />
                </div>
                
                <div class="col-md-6 mb-3">
                  <label for="lastName" class="form-label">Last Name</label>
                  <input
                    type="text"
                    class="form-control"
                    id="lastName"
                    v-model="form.lastName"
                    required
                  />
                </div>
              </div>
              
              <div class="mb-3">
                <label for="username" class="form-label">Username</label>
                <input
                  type="text"
                  class="form-control"
                  id="username"
                  v-model="form.username"
                  required
                />
              </div>
              
              <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input
                  type="email"
                  class="form-control"
                  id="email"
                  v-model="form.email"
                  required
                />
              </div>
              
              <div class="mb-3">
                <label for="phoneNumber" class="form-label">Phone Number</label>
                <input
                  type="tel"
                  class="form-control"
                  id="phoneNumber"
                  v-model="form.phoneNumber"
                  placeholder="Enter phone number (optional)"
                />
              </div>
              
              <div v-if="error" class="alert alert-danger">
                {{ error }}
              </div>
              
              <div v-if="success" class="alert alert-success">
                {{ success }}
              </div>
              
              <div class="d-flex gap-2">
                <button 
                  type="submit" 
                  class="btn btn-primary"
                  :disabled="updating || !isFormChanged"
                >
                  <span v-if="updating" class="spinner-border spinner-border-sm me-2"></span>
                  {{ updating ? 'Updating...' : 'Update Profile' }}
                </button>
                
                <button 
                  type="button" 
                  class="btn btn-outline-secondary"
                  @click="resetForm"
                  :disabled="updating"
                >
                  Reset
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Change Password Section -->
        <div class="card mt-4">
          <div class="card-header">
            <h5 class="mb-0">Change Password</h5>
          </div>
          <div class="card-body">
            <form @submit.prevent="changePassword">
              <div class="mb-3">
                <label for="currentPassword" class="form-label">Current Password</label>
                <input
                  type="password"
                  class="form-control"
                  id="currentPassword"
                  v-model="passwordForm.currentPassword"
                  required
                />
              </div>
              
              <div class="mb-3">
                <label for="newPassword" class="form-label">New Password</label>
                <input
                  type="password"
                  class="form-control"
                  id="newPassword"
                  v-model="passwordForm.newPassword"
                  required
                  minlength="6"
                />
                <div class="form-text">Password must be at least 6 characters long.</div>
              </div>
              
              <div class="mb-3">
                <label for="confirmPassword" class="form-label">Confirm New Password</label>
                <input
                  type="password"
                  class="form-control"
                  id="confirmPassword"
                  v-model="passwordForm.confirmPassword"
                  required
                />
              </div>
              
              <div v-if="passwordError" class="alert alert-danger">
                {{ passwordError }}
              </div>
              
              <div v-if="passwordSuccess" class="alert alert-success">
                {{ passwordSuccess }}
              </div>
              
              <button 
                type="submit" 
                class="btn btn-warning"
                :disabled="changingPassword || !isPasswordFormValid"
              >
                <span v-if="changingPassword" class="spinner-border spinner-border-sm me-2"></span>
                {{ changingPassword ? 'Changing...' : 'Change Password' }}
              </button>
            </form>
          </div>
        </div>

        <!-- Account Statistics -->
        <div class="card mt-4">
          <div class="card-header">
            <h5 class="mb-0">Account Statistics</h5>
          </div>
          <div class="card-body">
            <div class="row text-center">
              <div class="col-md-4 mb-3">
                <div class="stat-item">
                  <i class="fas fa-calendar-check fa-2x text-primary mb-2"></i>
                  <h4 class="mb-1">{{ stats.totalReservations }}</h4>
                  <p class="text-muted mb-0">Total Reservations</p>
                </div>
              </div>
              
              <div class="col-md-4 mb-3">
                <div class="stat-item">
                  <i class="fas fa-clock fa-2x text-success mb-2"></i>
                  <h4 class="mb-1">{{ stats.totalHours }}h</h4>
                  <p class="text-muted mb-0">Total Parking Hours</p>
                </div>
              </div>
              
              <div class="col-md-4 mb-3">
                <div class="stat-item">
                  <i class="fas fa-dollar-sign fa-2x text-warning mb-2"></i>
                  <h4 class="mb-1">${{ stats.totalSpent }}</h4>
                  <p class="text-muted mb-0">Total Amount Spent</p>
                </div>
              </div>
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
  name: 'UserProfile',
  data() {
    return {
      form: {
        firstName: '',
        lastName: '',
        username: '',
        email: '',
        phoneNumber: ''
      },
      passwordForm: {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      },
      originalForm: {},
      updating: false,
      changingPassword: false,
      error: null,
      success: null,
      passwordError: null,
      passwordSuccess: null,
      stats: {
        totalReservations: 0,
        totalHours: 0,
        totalSpent: 0
      }
    }
  },
  computed: {
    ...mapGetters('auth', ['user']),
    
    userFullName() {
      return this.user ? `${this.user.first_name} ${this.user.last_name}` : 'User'
    },
    
    isFormChanged() {
      return JSON.stringify(this.form) !== JSON.stringify(this.originalForm)
    },
    
    isPasswordFormValid() {
      return this.passwordForm.currentPassword &&
             this.passwordForm.newPassword &&
             this.passwordForm.confirmPassword &&
             this.passwordForm.newPassword === this.passwordForm.confirmPassword &&
             this.passwordForm.newPassword.length >= 6
    }
  },
  watch: {
    user: {
      immediate: true,
      handler(newUser) {
        if (newUser) {
          this.populateForm()
        }
      }
    }
  },
  async mounted() {
    await this.loadStats()
  },
  methods: {
    ...mapActions('auth', ['updateUserProfile', 'changeUserPassword']),
    ...mapActions('reservations', ['fetchUserReservations']),
    
    populateForm() {
      if (this.user) {
        this.form = {
          firstName: this.user.first_name || '',
          lastName: this.user.last_name || '',
          username: this.user.username || '',
          email: this.user.email || '',
          phoneNumber: this.user.phone_number || ''
        }
        this.originalForm = { ...this.form }
      }
    },
    
    resetForm() {
      this.form = { ...this.originalForm }
      this.error = null
      this.success = null
    },
    
    async updateProfile() {
      this.error = null
      this.success = null
      this.updating = true
      
      try {
        const updateData = {
          first_name: this.form.firstName,
          last_name: this.form.lastName,
          username: this.form.username,
          email: this.form.email,
          phone_number: this.form.phoneNumber || null
        }
        
        await this.updateUserProfile(updateData)
        this.originalForm = { ...this.form }
        this.success = 'Profile updated successfully!'
        
        // Clear success message after 3 seconds
        setTimeout(() => {
          this.success = null
        }, 3000)
        
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to update profile'
      } finally {
        this.updating = false
      }
    },
    
    async changePassword() {
      this.passwordError = null
      this.passwordSuccess = null
      
      // Validate passwords match
      if (this.passwordForm.newPassword !== this.passwordForm.confirmPassword) {
        this.passwordError = 'New passwords do not match'
        return
      }
      
      this.changingPassword = true
      
      try {
        await this.changeUserPassword({
          current_password: this.passwordForm.currentPassword,
          new_password: this.passwordForm.newPassword
        })
        
        // Clear form
        this.passwordForm = {
          currentPassword: '',
          newPassword: '',
          confirmPassword: ''
        }
        
        this.passwordSuccess = 'Password changed successfully!'
        
        // Clear success message after 3 seconds
        setTimeout(() => {
          this.passwordSuccess = null
        }, 3000)
        
      } catch (error) {
        this.passwordError = error.response?.data?.message || 'Failed to change password'
      } finally {
        this.changingPassword = false
      }
    },
    
    async loadStats() {
      try {
        const reservations = await this.fetchUserReservations()
        
        this.stats.totalReservations = reservations.length
        this.stats.totalHours = reservations
          .filter(r => r.duration_hours)
          .reduce((sum, r) => sum + parseFloat(r.duration_hours), 0)
          .toFixed(1)
        this.stats.totalSpent = reservations
          .filter(r => r.parking_cost)
          .reduce((sum, r) => sum + parseFloat(r.parking_cost), 0)
          .toFixed(2)
          
      } catch (error) {
        console.error('Error loading stats:', error)
      }
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
  border-radius: 12px;
  border: none;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.avatar-placeholder {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}

.avatar-placeholder i {
  color: white;
}

.stat-item {
  padding: 1rem;
  border-radius: 8px;
  background-color: #f8f9fa;
  height: 100%;
}

.btn {
  border-radius: 8px;
  font-weight: 500;
}

.form-control:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

.alert {
  border-radius: 8px;
}
</style>
