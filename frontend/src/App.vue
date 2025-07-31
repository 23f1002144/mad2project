<template>
  <div id="app">
    <!-- Navigation Bar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container">
        <router-link class="navbar-brand" to="/">
          <i class="fas fa-car"></i>
          ParkingApp V2
        </router-link>
        
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item" v-if="isAuthenticated">
              <router-link class="nav-link" :to="dashboardRoute">
                <i class="fas fa-tachometer-alt"></i>
                Dashboard
              </router-link>
            </li>
            <li class="nav-item" v-if="isUser">
              <router-link class="nav-link" to="/parking-lots">
                <i class="fas fa-parking"></i>
                Find Parking
              </router-link>
            </li>
            <li class="nav-item" v-if="isAdmin">
              <router-link class="nav-link" to="/admin/lots">
                <i class="fas fa-cogs"></i>
                Manage Lots
              </router-link>
            </li>
            <li class="nav-item" v-if="isAdmin">
              <router-link class="nav-link" to="/admin/users">
                <i class="fas fa-users"></i>
                Users
              </router-link>
            </li>
          </ul>
          
          <ul class="navbar-nav">
            <li class="nav-item" v-if="!isAuthenticated">
              <router-link class="nav-link" to="/login">
                <i class="fas fa-sign-in-alt"></i>
                Login
              </router-link>
            </li>
            <li class="nav-item" v-if="!isAuthenticated">
              <router-link class="nav-link" to="/register">
                <i class="fas fa-user-plus"></i>
                Register
              </router-link>
            </li>
            <li class="nav-item dropdown" v-if="isAuthenticated">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                <i class="fas fa-user"></i>
                {{ currentUser.first_name }}
              </a>
              <ul class="dropdown-menu">
                <li v-if="isUser">
                  <router-link class="dropdown-item" to="/profile">
                    <i class="fas fa-user-edit"></i>
                    Profile
                  </router-link>
                </li>
                <li v-if="isUser">
                  <router-link class="dropdown-item" to="/reservations">
                    <i class="fas fa-history"></i>
                    My Reservations
                  </router-link>
                </li>
                <li><hr class="dropdown-divider"></li>
                <li>
                  <a class="dropdown-item" href="#" @click="logout">
                    <i class="fas fa-sign-out-alt"></i>
                    Logout
                  </a>
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Alert Messages -->
    <div class="container mt-3" v-if="alertMessage">
      <div :class="`alert alert-${alertType} alert-dismissible fade show`" role="alert">
        {{ alertMessage }}
        <button type="button" class="btn-close" @click="clearAlert"></button>
      </div>
    </div>

    <!-- Main Content -->
    <main class="container-fluid py-4">
      <router-view />
    </main>

    <!-- Footer -->
    <footer class="bg-dark text-light text-center py-3 mt-5">
      <div class="container">
        <p>&copy; 2024 Vehicle Parking App V2. All rights reserved.</p>
        <p class="small">Built with Flask, Vue.js, and Bootstrap</p>
      </div>
    </footer>

    <!-- Loading Overlay -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex'

export default {
  name: 'App',
  computed: {
    ...mapState(['isLoading', 'alertMessage', 'alertType']),
    ...mapGetters(['isAuthenticated', 'isAdmin', 'isUser', 'currentUser']),
    
    dashboardRoute() {
      return this.isAdmin ? '/admin/dashboard' : '/dashboard'
    }
  },
  
  methods: {
    ...mapActions(['logout', 'clearAlert']),
    
    async logout() {
      try {
        await this.$store.dispatch('logout')
        this.$router.push('/login')
      } catch (error) {
        console.error('Logout error:', error)
      }
    }
  },
  
  created() {
    // Check authentication status on app load
    this.$store.dispatch('checkAuth')
  }
}
</script>

<style>
/* Loading overlay styles */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.loading-spinner {
  text-align: center;
}

/* Custom styles */
.navbar-brand {
  font-weight: bold;
}

.navbar-brand i {
  margin-right: 0.5rem;
}

main {
  min-height: calc(100vh - 200px);
}

/* Animation for route transitions */
.page-enter-active, .page-leave-active {
  transition: opacity 0.3s ease;
}

.page-enter-from, .page-leave-to {
  opacity: 0;
}

/* Alert animations */
.alert {
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    transform: translateY(-20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .container-fluid {
    padding-left: 1rem;
    padding-right: 1rem;
  }
}
</style>
