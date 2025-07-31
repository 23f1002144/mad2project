<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6 col-lg-5">
        <div class="card shadow">
          <div class="card-header bg-primary text-white text-center">
            <h3>Create Account</h3>
          </div>
          <div class="card-body">
            <form @submit.prevent="handleRegister">
              <div class="mb-3">
                <label for="firstName" class="form-label">First Name</label>
                <input
                  type="text"
                  class="form-control"
                  id="firstName"
                  v-model="form.firstName"
                  required
                />
              </div>
              
              <div class="mb-3">
                <label for="lastName" class="form-label">Last Name</label>
                <input
                  type="text"
                  class="form-control"
                  id="lastName"
                  v-model="form.lastName"
                  required
                />
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
                <label for="phoneNumber" class="form-label">Phone Number (Optional)</label>
                <input
                  type="tel"
                  class="form-control"
                  id="phoneNumber"
                  v-model="form.phoneNumber"
                />
              </div>
              
              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input
                  type="password"
                  class="form-control"
                  id="password"
                  v-model="form.password"
                  required
                />
              </div>
              
              <div class="mb-3">
                <label for="confirmPassword" class="form-label">Confirm Password</label>
                <input
                  type="password"
                  class="form-control"
                  id="confirmPassword"
                  v-model="form.confirmPassword"
                  required
                />
              </div>
              
              <div v-if="error" class="alert alert-danger">
                {{ error }}
              </div>
              
              <button 
                type="submit" 
                class="btn btn-primary w-100"
                :disabled="loading"
              >
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                {{ loading ? 'Creating Account...' : 'Register' }}
              </button>
            </form>
            
            <div class="text-center mt-3">
              <p class="mb-0">
                Already have an account? 
                <router-link to="/login" class="text-decoration-none">Sign in</router-link>
              </p>
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
  name: 'Register',
  data() {
    return {
      form: {
        firstName: '',
        lastName: '',
        username: '',
        email: '',
        phoneNumber: '',
        password: '',
        confirmPassword: ''
      },
      loading: false,
      error: null
    }
  },
  methods: {
    ...mapActions(['register']),
    
    async handleRegister() {
      this.error = null
      
      // Validate form
      if (this.form.password !== this.form.confirmPassword) {
        this.error = 'Passwords do not match'
        return
      }
      
      if (this.form.password.length < 6) {
        this.error = 'Password must be at least 6 characters long'
        return
      }
      
      this.loading = true
      
      try {
        const userData = {
          first_name: this.form.firstName,
          last_name: this.form.lastName,
          username: this.form.username,
          email: this.form.email,
          phone_number: this.form.phoneNumber || null,
          password: this.form.password
        }
        
        await this.$store.dispatch('register', userData)
        
        // Registration successful, redirect to dashboard
        const userType = this.$store.getters.userType
        const redirectPath = userType === 'admin' ? '/admin/dashboard' : '/dashboard'
        this.$router.push(redirectPath)
        
      } catch (error) {
        this.error = error.response?.data?.error || 'Registration failed. Please try again.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.card {
  border-radius: 10px;
}

.card-header {
  border-radius: 10px 10px 0 0;
}

.form-control:focus {
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
}
</style>
