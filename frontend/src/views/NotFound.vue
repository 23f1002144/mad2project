<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8 col-lg-6">
        <div class="text-center">
          <!-- 404 Illustration -->
          <div class="error-illustration mb-4">
            <div class="error-code">404</div>
            <div class="error-icon">
              <i class="fas fa-car-crash fa-4x text-muted"></i>
            </div>
          </div>
          
          <!-- Error Message -->
          <h1 class="display-4 fw-bold text-primary mb-3">Oops! Page Not Found</h1>
          <p class="lead text-muted mb-4">
            The page you're looking for seems to have driven off to another location. 
            Let's get you back on track!
          </p>
          
          <!-- Error Details -->
          <div class="alert alert-light border mb-4">
            <div class="row text-start">
              <div class="col-sm-6 mb-2">
                <strong>Current URL:</strong><br>
                <code class="text-danger">{{ currentPath }}</code>
              </div>
              <div class="col-sm-6 mb-2">
                <strong>Error Code:</strong><br>
                <span class="badge bg-danger">404 - Not Found</span>
              </div>
            </div>
          </div>
          
          <!-- Quick Actions -->
          <div class="d-grid gap-2 d-md-flex justify-content-md-center mb-4">
            <button @click="goBack" class="btn btn-outline-secondary me-md-2">
              <i class="fas fa-arrow-left me-2"></i>
              Go Back
            </button>
            <router-link to="/" class="btn btn-primary">
              <i class="fas fa-home me-2"></i>
              Go Home
            </router-link>
            <router-link 
              v-if="isAuthenticated" 
              :to="userType === 'admin' ? '/admin/dashboard' : '/dashboard'" 
              class="btn btn-success"
            >
              <i class="fas fa-tachometer-alt me-2"></i>
              Dashboard
            </router-link>
          </div>
          
          <!-- Helpful Links -->
          <div class="card">
            <div class="card-header">
              <h5 class="mb-0">
                <i class="fas fa-compass me-2"></i>
                Need Help Finding Your Way?
              </h5>
            </div>
            <div class="card-body">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <h6 class="text-primary">For Users:</h6>
                  <ul class="list-unstyled">
                    <li>
                      <router-link to="/parking-lots" class="text-decoration-none">
                        <i class="fas fa-search me-2"></i>Find Parking
                      </router-link>
                    </li>
                    <li>
                      <router-link to="/reservations" class="text-decoration-none">
                        <i class="fas fa-calendar-check me-2"></i>My Reservations
                      </router-link>
                    </li>
                    <li>
                      <router-link to="/profile" class="text-decoration-none">
                        <i class="fas fa-user me-2"></i>My Profile
                      </router-link>
                    </li>
                  </ul>
                </div>
                <div class="col-md-6 mb-3">
                  <h6 class="text-success">For Admins:</h6>
                  <ul class="list-unstyled">
                    <li>
                      <router-link to="/admin/lots" class="text-decoration-none">
                        <i class="fas fa-building me-2"></i>Manage Lots
                      </router-link>
                    </li>
                    <li>
                      <router-link to="/admin/users" class="text-decoration-none">
                        <i class="fas fa-users me-2"></i>Manage Users
                      </router-link>
                    </li>
                    <li>
                      <router-link to="/admin/reservations" class="text-decoration-none">
                        <i class="fas fa-calendar-alt me-2"></i>View Reservations
                      </router-link>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Footer Message -->
          <div class="mt-4">
            <p class="text-muted small">
              If you believe this is an error, please contact support or try refreshing the page.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'NotFound',
  computed: {
    ...mapGetters('auth', ['isAuthenticated', 'userType']),
    
    currentPath() {
      return this.$route.fullPath
    }
  },
  methods: {
    goBack() {
      // Check if there's a previous page in history
      if (window.history.length > 1) {
        this.$router.go(-1)
      } else {
        // If no history, go to home
        this.$router.push('/')
      }
    }
  },
  mounted() {
    // Track 404 errors for analytics (if implemented)
    console.warn('404 Error - Page not found:', this.currentPath)
  }
}
</script>

<style scoped>
.error-illustration {
  position: relative;
  margin-bottom: 2rem;
}

.error-code {
  font-size: 8rem;
  font-weight: 900;
  color: #e9ecef;
  line-height: 1;
  position: relative;
  z-index: 1;
}

.error-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 2;
}

.card {
  border-radius: 12px;
  border: none;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.card-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px 12px 0 0;
}

.btn {
  border-radius: 8px;
  font-weight: 500;
}

.alert {
  border-radius: 8px;
}

code {
  background-color: #f8f9fa;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.9rem;
}

.list-unstyled li {
  margin-bottom: 0.5rem;
}

.list-unstyled a {
  color: #6c757d;
  transition: color 0.2s;
}

.list-unstyled a:hover {
  color: #495057;
}

@media (max-width: 768px) {
  .error-code {
    font-size: 5rem;
  }
  
  .error-icon {
    font-size: 2rem;
  }
  
  .display-4 {
    font-size: 2rem;
  }
}
</style>
