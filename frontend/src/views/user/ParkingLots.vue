<template>
    <div class="container-fluid py-4">
    <!-- Success Alert -->
    <div v-if="showSuccessAlert" class="alert alert-success alert-dismissible fade show mb-4" role="alert">
      <i class="fas fa-check-circle me-2"></i>
      <strong>Success!</strong> {{ successMessage }}
      <button type="button" class="btn-close" @click="showSuccessAlert = false"></button>
    </div>

    <!-- Error Alert -->
    <div v-if="showErrorAlert" class="alert alert-danger alert-dismissible fade show mb-4" role="alert">
      <i class="fas fa-exclamation-circle me-2"></i>
      <strong>Error!</strong> {{ errorMessage }}
      <button type="button" class="btn-close" @click="showErrorAlert = false"></button>
    </div>

    <!-- Header -->
    <div class="row mb-4">
      <div class="col">
        <h2 class="h3 mb-0">
          <i class="fas fa-car me-2 text-primary"></i>
          Available Parking Lots
        </h2>
        <p class="text-muted mb-0">Find and reserve a parking spot</p>
      </div>
      <div class="col-auto">
        <button @click="refreshLots" class="btn btn-outline-primary" :disabled="loading">
          <i class="fas fa-sync-alt me-2" :class="{ 'fa-spin': loading }"></i>
          Refresh
        </button>
      </div>
    </div>

    <!-- Search and Filter -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="card">
          <div class="card-body">
            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="search" class="form-label">Search by location or address</label>
                <input
                  type="text"
                  class="form-control"
                  id="search"
                  v-model="searchQuery"
                  placeholder="Enter location name or address..."
                />
              </div>
              <div class="col-md-3 mb-3">
                <label for="maxPrice" class="form-label">Max Price per Hour</label>
                <input
                  type="number"
                  class="form-control"
                  id="maxPrice"
                  v-model="maxPrice"
                  placeholder="Enter max price"
                  min="0"
                  step="0.5"
                />
              </div>
              <div class="col-md-3 mb-3">
                <label for="sortBy" class="form-label">Sort by</label>
                <select class="form-select" id="sortBy" v-model="sortBy">
                  <option value="name">Location Name</option>
                  <option value="price">Price (Low to High)</option>
                  <option value="available_spots">Available Spots</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3 text-muted">Loading parking lots...</p>
    </div>

    <!-- No Results -->
    <div v-else-if="filteredLots.length === 0" class="text-center py-5">
      <i class="fas fa-search fa-3x text-muted mb-3"></i>
      <h4 class="text-muted">No parking lots found</h4>
      <p class="text-muted">Try adjusting your search criteria or refresh the page.</p>
    </div>

    <!-- Parking Lots Grid -->
    <div v-else class="row">
      <div v-for="lot in filteredLots" :key="lot.id" class="col-lg-6 col-xl-4 mb-4">
        <div class="card h-100 lot-card">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-3">
              <h5 class="card-title text-primary">{{ lot.prime_location_name }}</h5>
              <span 
                class="badge"
                :class="lot.available_spots > 0 ? 'bg-success' : 'bg-danger'"
              >
                {{ lot.available_spots > 0 ? 'Available' : 'Full' }}
              </span>
            </div>
            
            <div class="mb-3">
              <p class="card-text text-muted mb-2">
                <i class="fas fa-map-marker-alt me-2"></i>
                {{ lot.address }}
              </p>
              <p class="card-text text-muted mb-2">
                <i class="fas fa-mail-bulk me-2"></i>
                {{ lot.pin_code }}
              </p>
            </div>

            <div class="row mb-3">
              <div class="col-6">
                <div class="text-center">
                  <div class="h4 text-success mb-0">{{ lot.available_spots }}</div>
                  <small class="text-muted">Available</small>
                </div>
              </div>
              <div class="col-6">
                <div class="text-center">
                  <div class="h4 text-warning mb-0">${{ lot.price_per_hour }}</div>
                  <small class="text-muted">per hour</small>
                </div>
              </div>
            </div>

            <div class="mb-3">
              <div class="progress" style="height: 8px;">
                <div 
                  class="progress-bar bg-success" 
                  :style="{ width: getOccupancyPercentage(lot) + '%' }"
                ></div>
              </div>
              <small class="text-muted">
                {{ lot.occupied_spots }}/{{ lot.number_of_spots }} spots occupied
              </small>
            </div>

            <div v-if="lot.description" class="mb-3">
              <p class="card-text small text-muted">{{ lot.description }}</p>
            </div>
          </div>

          <div class="card-footer bg-transparent">
            <button
              @click="reserveSpot(lot)"
              class="btn btn-primary w-100"
              :disabled="lot.available_spots === 0 || reserving === lot.id"
            >
              <span v-if="reserving === lot.id" class="spinner-border spinner-border-sm me-2"></span>
              {{ reserving === lot.id ? 'Reserving...' : 'Reserve Spot' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Reservation Modal -->
    <div class="modal fade" id="reservationModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Reserve Parking Spot</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div v-if="selectedLot">
              <h6>{{ selectedLot.prime_location_name }}</h6>
              <p class="text-muted">{{ selectedLot.address }}</p>
              
              <form @submit.prevent="confirmReservation">
                <div class="mb-3">
                  <label for="vehicleNumber" class="form-label">Vehicle Number</label>
                  <input
                    type="text"
                    class="form-control"
                    id="vehicleNumber"
                    v-model="reservationForm.vehicleNumber"
                    placeholder="Enter your vehicle number"
                    required
                  />
                </div>
                
                <div class="mb-3">
                  <label for="remarks" class="form-label">Remarks (Optional)</label>
                  <textarea
                    class="form-control"
                    id="remarks"
                    v-model="reservationForm.remarks"
                    rows="3"
                    placeholder="Any special instructions or remarks..."
                  ></textarea>
                </div>
                
                <div class="alert alert-info">
                  <i class="fas fa-info-circle me-2"></i>
                  Rate: ${{ selectedLot.price_per_hour }} per hour
                </div>
              </form>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button 
              type="button" 
              class="btn btn-primary"
              @click="confirmReservation"
              :disabled="!reservationForm.vehicleNumber || reserving"
            >
              <span v-if="reserving" class="spinner-border spinner-border-sm me-2"></span>
              {{ reserving ? 'Reserving...' : 'Confirm Reservation' }}
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
  name: 'ParkingLots',
  data() {
    return {
      loading: false,
      reserving: null,
      parkingLots: [],
      searchQuery: '',
      maxPrice: null,
      sortBy: 'name',
      selectedLot: null,
      reservationForm: {
        vehicleNumber: '',
        remarks: ''
      },
      showSuccessAlert: false,
      showErrorAlert: false,
      successMessage: '',
      errorMessage: ''
    }
  },
  computed: {
    filteredLots() {
      let filtered = this.parkingLots.filter(lot => {
        // Filter by search query
        const matchesSearch = !this.searchQuery || 
          lot.prime_location_name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          lot.address.toLowerCase().includes(this.searchQuery.toLowerCase())
        
        // Filter by max price
        const matchesPrice = !this.maxPrice || lot.price_per_hour <= parseFloat(this.maxPrice)
        
        // Only show active lots with available spots
        const isAvailable = lot.is_active && lot.available_spots > 0
        
        return matchesSearch && matchesPrice && isAvailable
      })
      
      // Sort results
      return filtered.sort((a, b) => {
        switch (this.sortBy) {
          case 'price':
            return a.price_per_hour - b.price_per_hour
          case 'available_spots':
            return b.available_spots - a.available_spots
          default:
            return a.prime_location_name.localeCompare(b.prime_location_name)
        }
      })
    }
  },
  async mounted() {
    await this.loadParkingLots()
  },
  methods: {
    ...mapActions('parking', ['fetchParkingLots', 'createReservation']),
    
    async loadParkingLots() {
      this.loading = true
      try {
        this.parkingLots = await this.fetchParkingLots()
      } catch (error) {
        console.error('Error loading parking lots:', error)
        this.showError('Failed to load parking lots')
      } finally {
        this.loading = false
      }
    },
    
    async refreshLots() {
      await this.loadParkingLots()
    },
    
    showSuccess(message) {
      this.successMessage = message
      this.showSuccessAlert = true
      this.showErrorAlert = false
      // Auto-hide after 5 seconds
      setTimeout(() => {
        this.showSuccessAlert = false
      }, 5000)
    },
    
    showError(message) {
      this.errorMessage = message
      this.showErrorAlert = true
      this.showSuccessAlert = false
      // Auto-hide after 8 seconds
      setTimeout(() => {
        this.showErrorAlert = false
      }, 8000)
    },
    
    getOccupancyPercentage(lot) {
      if (lot.number_of_spots === 0) return 0
      return Math.round((lot.occupied_spots / lot.number_of_spots) * 100)
    },
    
    reserveSpot(lot) {
      this.selectedLot = lot
      this.reservationForm = {
        vehicleNumber: '',
        remarks: ''
      }
      
      // Show modal
      const modal = new window.bootstrap.Modal(document.getElementById('reservationModal'))
      modal.show()
    },
    
    async confirmReservation() {
      if (!this.reservationForm.vehicleNumber.trim()) {
        this.showError('Please enter vehicle number')
        return
      }
      
      this.reserving = this.selectedLot.id
      
      try {
        const reservationData = {
          lotId: this.selectedLot.id,
          vehicleNumber: this.reservationForm.vehicleNumber.trim(),
          remarks: this.reservationForm.remarks.trim() || null
        }
        
        await this.createReservation(reservationData)
        
        // Hide modal
        const modal = window.bootstrap.Modal.getInstance(document.getElementById('reservationModal'))
        modal.hide()
        
        // Refresh lots to update availability
        await this.loadParkingLots()
        
        // Show success message
        this.showSuccess(`Parking spot reserved successfully at ${this.selectedLot.prime_location_name}!`)
        
        // Redirect to reservations page after showing success message
        setTimeout(() => {
          this.$router.push('/reservations')
        }, 2000)
        
      } catch (error) {
        console.error('Error creating reservation:', error)
        this.showError(error.response?.data?.message || 'Failed to reserve parking spot')
      } finally {
        this.reserving = null
      }
    }
  }
}
</script>

<style scoped>
.lot-card {
  border: none;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: transform 0.2s, box-shadow 0.2s;
  border-radius: 12px;
}

.lot-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}

.card-title {
  font-weight: 600;
}

.progress {
  border-radius: 4px;
}

.badge {
  font-size: 0.75rem;
  padding: 0.5em 0.75em;
}

.btn {
  border-radius: 8px;
  font-weight: 500;
}

.modal-content {
  border-radius: 12px;
  border: none;
}

.modal-header {
  border-bottom: 1px solid #e9ecef;
  border-radius: 12px 12px 0 0;
}

.modal-footer {
  border-top: 1px solid #e9ecef;
  border-radius: 0 0 12px 12px;
}

.fa-spin {
  animation: fa-spin 1s infinite linear;
}

@keyframes fa-spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
