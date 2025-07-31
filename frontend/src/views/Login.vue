<template>
  <div class="login-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
          <div class="login-card card shadow-lg border-0">
            <div class="card-header bg-primary text-white text-center py-4">
              <h3 class="mb-0">
                <i class="fas fa-car me-2"></i>
                ParkingApp Login
              </h3>
            </div>
            
            <div class="card-body p-4">
              <form @submit.prevent="handleLogin">
                <!-- Username Field -->
                <div class="mb-3">
                  <label for="username" class="form-label">
                    <i class="fas fa-user me-1"></i>
                    Username
                  </label>
                  <input
                    type="text"
                    id="username"
                    v-model="username"
                    class="form-control form-control-lg"
                    placeholder="Enter your username"
                    required
                    :disabled="isLoading"
                  >
                </div>

                <!-- Password Field -->
                <div class="mb-4">
                  <label for="password" class="form-label">
                    <i class="fas fa-lock me-1"></i>
                    Password
                  </label>
                  <div class="input-group input-group-lg">
                    <input
                      :type="showPassword ? 'text' : 'password'"
                      id="password"
                      v-model="password"
                      class="form-control"
                      placeholder="Enter your password"
                      required
                      :disabled="isLoading"
                    >
                    <button
                      type="button"
                      class="btn btn-outline-secondary"
                      @click="showPassword = !showPassword"
                      :disabled="isLoading"
                    >
                      <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                    </button>
                  </div>
                </div>

                <!-- Login Button -->
                <button
                  type="submit"
                  class="btn btn-primary btn-lg w-100 mb-3"
                  :disabled="isLoading || !isFormValid"
                >
                  <span v-if="isLoading">
                    <i class="fas fa-spinner fa-spin me-2"></i>
                    Logging in...
                  </span>
                  <span v-else>
                    <i class="fas fa-sign-in-alt me-2"></i>
                    Login
                  </span>
                </button>

                <!-- Demo Credentials -->
                <div class="demo-credentials bg-light p-3 rounded mb-3">
                  <h6 class="text-muted mb-2">
                    <i class="fas fa-info-circle me-1"></i>
                    Demo Credentials:
                  </h6>
                  <div class="row g-2">
                    <div class="col-6">
                      <small class="d-block">
                        <strong>Admin:</strong><br>
                        Username: admin<br>
                        Password: admin123
                      </small>
                    </div>
                    <div class="col-6">
                      <small class="d-block">
                        <strong>User:</strong><br>
                        Username: john_doe<br>
                        Password: user123
                      </small>
                    </div>
                  </div>
                  <div class="mt-2">
                    <button
                      type="button"
                      class="btn btn-sm btn-outline-secondary me-2"
                      @click="fillAdminCredentials"
                      :disabled="isLoading"
                    >
                      Use Admin
                    </button>
                    <button
                      type="button"
                      class="btn btn-sm btn-outline-secondary"
                      @click="fillUserCredentials"
                      :disabled="isLoading"
                    >
                      Use User
                    </button>
                  </div>
                </div>

                <!-- Register Link -->
                <div class="text-center">
                  <p class="text-muted mb-0">
                    Don't have an account?
                    <router-link to="/register" class="text-primary text-decoration-none">
                      Register here
                    </router-link>
                  </p>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'Login',
  
  data() {
    return {
      username: '',
      password: '',
      showPassword: false
    }
  },
  
  computed: {
    ...mapState(['isLoading']),
    
    isFormValid() {
      return this.username.trim() && this.password.trim()
    }
  },
  
  methods: {
    ...mapActions(['login']),
    
    async handleLogin() {
      if (!this.isFormValid) return
      
      try {
        const result = await this.login({
          username: this.username.trim(),
          password: this.password
        })
        
        // Redirect based on user type returned from server
        const redirectPath = result.user_type === 'admin' ? '/admin/dashboard' : '/dashboard'
        this.$router.push(redirectPath)
        
      } catch (error) {
        // Error is handled by the store
      }
    },
    
    fillAdminCredentials() {
      this.username = 'admin'
      this.password = 'admin123'
    },
    
    fillUserCredentials() {
      this.username = 'john_doe'
      this.password = 'user123'
    }
  },
  
  // Auto-redirect if already logged in
  created() {
    if (this.$store.getters.isAuthenticated) {
      const userType = this.$store.getters.userType
      const redirectPath = userType === 'admin' ? '/admin/dashboard' : '/dashboard'
      this.$router.push(redirectPath)
    }
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  padding: 2rem 0;
}

.login-card {
  border-radius: 15px;
  overflow: hidden;
  backdrop-filter: blur(10px);
}

.card-header {
  border-bottom: none;
}

.btn-check:checked + .btn {
  background-color: var(--bs-primary);
  border-color: var(--bs-primary);
  color: white;
}

.btn-check:checked + .btn.btn-outline-danger {
  background-color: var(--bs-danger);
  border-color: var(--bs-danger);
  color: white;
}

.form-control:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

.demo-credentials {
  border: 1px dashed #dee2e6;
}

.input-group-lg .btn {
  padding: 0.75rem 1rem;
}

/* Animation for form elements */
.login-card {
  animation: slideUp 0.6s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive adjustments */
@media (max-width: 576px) {
  .login-page {
    padding: 1rem 0;
  }
  
  .card-body {
    padding: 1.5rem !important;
  }
  
  .demo-credentials {
    font-size: 0.85rem;
  }
}
</style>
