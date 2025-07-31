<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero-section bg-primary text-white py-5">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-lg-6">
            <h1 class="display-4 fw-bold mb-4">
              <i class="fas fa-car me-3"></i>
              Smart Parking Made Easy
            </h1>
            <p class="lead mb-4">
              Find, reserve, and manage parking spots with our advanced parking management system. 
              Available 24/7 with real-time availability and seamless booking.
            </p>
            <div class="d-flex gap-3">
              <router-link to="/register" class="btn btn-light btn-lg">
                <i class="fas fa-user-plus me-2"></i>
                Get Started
              </router-link>
              <router-link to="/login" class="btn btn-outline-light btn-lg">
                <i class="fas fa-sign-in-alt me-2"></i>
                Login
              </router-link>
            </div>
          </div>
          <div class="col-lg-6 text-center">
            <div class="hero-icon">
              <i class="fas fa-parking fa-10x opacity-75"></i>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section py-5">
      <div class="container">
        <div class="row text-center mb-5">
          <div class="col-12">
            <h2 class="display-5 fw-bold mb-3">Why Choose Our Parking App?</h2>
            <p class="lead text-muted">Experience the future of parking management</p>
          </div>
        </div>
        
        <div class="row g-4">
          <div class="col-md-4">
            <div class="feature-card card h-100 border-0 shadow">
              <div class="card-body text-center p-4">
                <div class="feature-icon text-primary mb-3">
                  <i class="fas fa-search fa-3x"></i>
                </div>
                <h5 class="card-title">Find Parking Instantly</h5>
                <p class="card-text text-muted">
                  Search and find available parking spots in real-time across multiple locations.
                </p>
              </div>
            </div>
          </div>
          
          <div class="col-md-4">
            <div class="feature-card card h-100 border-0 shadow">
              <div class="card-body text-center p-4">
                <div class="feature-icon text-success mb-3">
                  <i class="fas fa-calendar-check fa-3x"></i>
                </div>
                <h5 class="card-title">Easy Reservations</h5>
                <p class="card-text text-muted">
                  Book your parking spot in advance or find immediate availability with just a few clicks.
                </p>
              </div>
            </div>
          </div>
          
          <div class="col-md-4">
            <div class="feature-card card h-100 border-0 shadow">
              <div class="card-body text-center p-4">
                <div class="feature-icon text-info mb-3">
                  <i class="fas fa-chart-line fa-3x"></i>
                </div>
                <h5 class="card-title">Smart Analytics</h5>
                <p class="card-text text-muted">
                  Track your parking history, expenses, and get insights to optimize your parking habits.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Statistics Section -->
    <section class="stats-section bg-light py-5" v-if="stats">
      <div class="container">
        <div class="row text-center">
          <div class="col-12 mb-4">
            <h3 class="fw-bold">Our Platform at a Glance</h3>
          </div>
        </div>
        <div class="row g-4">
          <div class="col-md-3 col-sm-6">
            <div class="stat-card card border-0 bg-primary text-white">
              <div class="card-body text-center">
                <i class="fas fa-parking fa-2x mb-2"></i>
                <h4 class="fw-bold">{{ stats.total_lots || 0 }}</h4>
                <p class="mb-0">Parking Lots</p>
              </div>
            </div>
          </div>
          <div class="col-md-3 col-sm-6">
            <div class="stat-card card border-0 bg-success text-white">
              <div class="card-body text-center">
                <i class="fas fa-square-parking fa-2x mb-2"></i>
                <h4 class="fw-bold">{{ stats.total_spots || 0 }}</h4>
                <p class="mb-0">Parking Spots</p>
              </div>
            </div>
          </div>
          <div class="col-md-3 col-sm-6">
            <div class="stat-card card border-0 bg-info text-white">
              <div class="card-body text-center">
                <i class="fas fa-users fa-2x mb-2"></i>
                <h4 class="fw-bold">{{ stats.total_users || 0 }}</h4>
                <p class="mb-0">Happy Users</p>
              </div>
            </div>
          </div>
          <div class="col-md-3 col-sm-6">
            <div class="stat-card card border-0 bg-warning text-white">
              <div class="card-body text-center">
                <i class="fas fa-calendar-check fa-2x mb-2"></i>
                <h4 class="fw-bold">{{ stats.total_reservations || 0 }}</h4>
                <p class="mb-0">Reservations</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section class="how-it-works py-5">
      <div class="container">
        <div class="row text-center mb-5">
          <div class="col-12">
            <h2 class="display-5 fw-bold mb-3">How It Works</h2>
            <p class="lead text-muted">Get started in three simple steps</p>
          </div>
        </div>
        
        <div class="row g-4">
          <div class="col-md-4">
            <div class="step-card text-center">
              <div class="step-number bg-primary text-white rounded-circle mx-auto mb-3 d-flex align-items-center justify-content-center">
                <span class="fw-bold fs-4">1</span>
              </div>
              <h5 class="fw-bold">Register & Login</h5>
              <p class="text-muted">
                Create your account and login to access all parking features.
              </p>
            </div>
          </div>
          
          <div class="col-md-4">
            <div class="step-card text-center">
              <div class="step-number bg-success text-white rounded-circle mx-auto mb-3 d-flex align-items-center justify-content-center">
                <span class="fw-bold fs-4">2</span>
              </div>
              <h5 class="fw-bold">Find & Reserve</h5>
              <p class="text-muted">
                Search available parking spots and make instant reservations.
              </p>
            </div>
          </div>
          
          <div class="col-md-4">
            <div class="step-card text-center">
              <div class="step-number bg-info text-white rounded-circle mx-auto mb-3 d-flex align-items-center justify-content-center">
                <span class="fw-bold fs-4">3</span>
              </div>
              <h5 class="fw-bold">Park & Pay</h5>
              <p class="text-muted">
                Park your vehicle and pay automatically based on usage time.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section bg-dark text-white py-5">
      <div class="container text-center">
        <h2 class="display-5 fw-bold mb-3">Ready to Start Parking Smart?</h2>
        <p class="lead mb-4">Join thousands of users who have simplified their parking experience</p>
        <router-link to="/register" class="btn btn-primary btn-lg me-3">
          <i class="fas fa-rocket me-2"></i>
          Get Started Now
        </router-link>
        <router-link to="/login" class="btn btn-outline-light btn-lg">
          <i class="fas fa-sign-in-alt me-2"></i>
          I Have an Account
        </router-link>
      </div>
    </section>
  </div>
</template>

<script>
import api from '@/services/api'

export default {
  name: 'Home',
  
  data() {
    return {
      stats: null
    }
  },
  
  async created() {
    await this.fetchStats()
  },
  
  methods: {
    async fetchStats() {
      try {
        // Fetch public statistics (if available)
        const response = await api.get('/parking/availability')
        
        // Calculate basic stats from availability data
        if (response.data.availability) {
          const availability = response.data.availability
          this.stats = {
            total_lots: availability.length,
            total_spots: availability.reduce((sum, lot) => sum + lot.total_spots, 0),
            total_users: 150, // Placeholder
            total_reservations: 1200 // Placeholder
          }
        }
      } catch (error) {
        // If API call fails, show placeholder stats
        this.stats = {
          total_lots: 5,
          total_spots: 455,
          total_users: 150,
          total_reservations: 1200
        }
      }
    }
  }
}
</script>

<style scoped>
.hero-section {
  min-height: 70vh;
  display: flex;
  align-items: center;
}

.hero-icon {
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
}

.feature-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 10px 25px rgba(0,0,0,0.1) !important;
}

.stat-card {
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: scale(1.05);
}

.step-number {
  width: 60px;
  height: 60px;
  font-size: 1.5rem;
}

.step-card {
  padding: 2rem 1rem;
}

.feature-icon {
  transition: transform 0.3s ease;
}

.feature-card:hover .feature-icon {
  transform: scale(1.1);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .hero-section {
    min-height: 60vh;
  }
  
  .display-4 {
    font-size: 2.5rem;
  }
  
  .hero-icon {
    margin-top: 2rem;
  }
  
  .btn-lg {
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
  }
}
</style>
