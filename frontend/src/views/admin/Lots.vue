<template>
  <div class="container-fluid mt-4">
    <!-- Page Header -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center">
          <h2>Manage Parking Lots</h2>
          <button @click="showCreateModal" class="btn btn-primary">
            <i class="fas fa-plus me-2"></i>
            Add New Lot
          </button>
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
                <label for="search" class="form-label">Search Lots</label>
                <input
                  type="text"
                  class="form-control"
                  id="search"
                  v-model="searchQuery"
                  placeholder="Search by name or address..."
                />
              </div>
              <div class="col-md-4 mb-3">
                <label for="statusFilter" class="form-label">Status</label>
                <select class="form-select" id="statusFilter" v-model="statusFilter">
                  <option value="">All Status</option>
                  <option value="active">Active</option>
                  <option value="inactive">Inactive</option>
                </select>
              </div>
              <div class="col-md-4 mb-3">
                <label for="sortBy" class="form-label">Sort By</label>
                <select class="form-select" id="sortBy" v-model="sortBy">
                  <option value="name">Name</option>
                  <option value="spots">Number of Spots</option>
                  <option value="price">Price per Hour</option>
                  <option value="occupancy">Occupancy Rate</option>
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

    <!-- Parking Lots Table -->
    <div v-else class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">Parking Lots ({{ filteredLots.length }})</h5>
          </div>
          <div class="card-body p-0">
            <div v-if="filteredLots.length === 0" class="text-center py-5">
              <i class="fas fa-search fa-3x text-muted mb-3"></i>
              <h5 class="text-muted">No parking lots found</h5>
              <p class="text-muted">Try adjusting your search criteria or add a new parking lot.</p>
            </div>
            <div v-else class="table-responsive">
              <table class="table table-hover mb-0">
                <thead class="bg-light">
                  <tr>
                    <th>Location Name</th>
                    <th>Address</th>
                    <th>Spots</th>
                    <th>Price/Hour</th>
                    <th>Occupancy</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="lot in filteredLots" :key="lot.id">
                    <td>
                      <div class="fw-bold">{{ lot.prime_location_name }}</div>
                      <small class="text-muted">ID: {{ lot.id }}</small>
                    </td>
                    <td>
                      <div>{{ lot.address }}</div>
                      <small class="text-muted">{{ lot.pin_code }}</small>
                    </td>
                    <td>
                      <div class="text-center">
                        <div class="fw-bold">{{ lot.number_of_spots }}</div>
                        <small class="text-success">{{ lot.available_spots }} available</small>
                      </div>
                    </td>
                    <td>
                      <span class="badge bg-warning text-dark">${{ lot.price_per_hour }}</span>
                    </td>
                    <td>
                      <div class="progress" style="height: 20px;">
                        <div 
                          class="progress-bar" 
                          :class="{
                            'bg-success': getOccupancyRate(lot) < 50,
                            'bg-warning': getOccupancyRate(lot) >= 50 && getOccupancyRate(lot) < 80,
                            'bg-danger': getOccupancyRate(lot) >= 80
                          }"
                          :style="{ width: getOccupancyRate(lot) + '%' }"
                        >
                          {{ getOccupancyRate(lot) }}%
                        </div>
                      </div>
                    </td>
                    <td>
                      <span 
                        class="badge"
                        :class="lot.is_active ? 'bg-success' : 'bg-secondary'"
                      >
                        {{ lot.is_active ? 'Active' : 'Inactive' }}
                      </span>
                    </td>
                    <td>
                      <div class="btn-group" role="group">
                        <button 
                          @click="editLot(lot)" 
                          class="btn btn-sm btn-outline-primary"
                          title="Edit"
                        >
                          <i class="fas fa-edit"></i>
                        </button>
                        <button 
                          @click="manageLotSpots(lot)" 
                          class="btn btn-sm btn-outline-info"
                          title="Manage Spots"
                        >
                          <i class="fas fa-car"></i>
                        </button>
                        <button 
                          @click="toggleLotStatus(lot)" 
                          class="btn btn-sm"
                          :class="lot.is_active ? 'btn-outline-warning' : 'btn-outline-success'"
                          :title="lot.is_active ? 'Deactivate' : 'Activate'"
                          :disabled="actionLoading === lot.id"
                        >
                          <span v-if="actionLoading === lot.id" class="spinner-border spinner-border-sm"></span>
                          <i v-else class="fas" :class="lot.is_active ? 'fa-pause' : 'fa-play'"></i>
                        </button>
                        <button 
                          @click="deleteLot(lot)" 
                          class="btn btn-sm btn-outline-danger"
                          title="Delete"
                          :disabled="actionLoading === lot.id"
                        >
                          <i class="fas fa-trash"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Lot Modal -->
    <div class="modal fade" id="lotModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ isEditing ? 'Edit' : 'Create New' }} Parking Lot</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveLot">
              <div class="row">
                <div class="col-md-8 mb-3">
                  <label for="locationName" class="form-label">Location Name</label>
                  <input
                    type="text"
                    class="form-control"
                    id="locationName"
                    v-model="lotForm.prime_location_name"
                    required
                  />
                </div>
                <div class="col-md-4 mb-3">
                  <label for="pinCode" class="form-label">Pin Code</label>
                  <input
                    type="text"
                    class="form-control"
                    id="pinCode"
                    v-model="lotForm.pin_code"
                    required
                  />
                </div>
              </div>
              
              <div class="mb-3">
                <label for="address" class="form-label">Address</label>
                <textarea
                  class="form-control"
                  id="address"
                  v-model="lotForm.address"
                  rows="3"
                  required
                ></textarea>
              </div>
              
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="numberOfSpots" class="form-label">Number of Spots</label>
                  <input
                    type="number"
                    class="form-control"
                    id="numberOfSpots"
                    v-model="lotForm.number_of_spots"
                    min="1"
                    required
                  />
                </div>
                <div class="col-md-6 mb-3">
                  <label for="pricePerHour" class="form-label">Price per Hour ($)</label>
                  <input
                    type="number"
                    class="form-control"
                    id="pricePerHour"
                    v-model="lotForm.price_per_hour"
                    min="0"
                    step="0.50"
                    required
                  />
                </div>
              </div>
              
              <div class="mb-3">
                <label for="description" class="form-label">Description (Optional)</label>
                <textarea
                  class="form-control"
                  id="description"
                  v-model="lotForm.description"
                  rows="2"
                  placeholder="Additional information about the parking lot..."
                ></textarea>
              </div>
              
              <div class="mb-3">
                <div class="form-check">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    id="isActive"
                    v-model="lotForm.is_active"
                  />
                  <label class="form-check-label" for="isActive">
                    Active (Available for reservations)
                  </label>
                </div>
              </div>
              
              <div v-if="formError" class="alert alert-danger">
                {{ formError }}
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button 
              type="button" 
              class="btn btn-primary"
              @click="saveLot"
              :disabled="saving"
            >
              <span v-if="saving" class="spinner-border spinner-border-sm me-2"></span>
              {{ saving ? 'Saving...' : (isEditing ? 'Update' : 'Create') }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Manage Spots Modal -->
    <div class="modal fade" id="spotsModal" tabindex="-1">
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Manage Spots - {{ selectedLot?.prime_location_name }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div v-if="selectedLot">
              <div class="row mb-3">
                <div class="col-md-6">
                  <h6>Lot Information</h6>
                  <p><strong>Total Spots:</strong> {{ selectedLot.number_of_spots }}</p>
                  <p><strong>Available:</strong> {{ selectedLot.available_spots }}</p>
                  <p><strong>Occupied:</strong> {{ selectedLot.occupied_spots }}</p>
                </div>
                <div class="col-md-6">
                  <button @click="generateSpots" class="btn btn-warning me-2" :disabled="generatingSpots">
                    <span v-if="generatingSpots" class="spinner-border spinner-border-sm me-2"></span>
                    Generate Missing Spots
                  </button>
                  <button @click="loadLotSpots" class="btn btn-outline-primary">
                    <i class="fas fa-sync-alt me-2"></i>Refresh
                  </button>
                </div>
              </div>
              
              <div v-if="loadingSpots" class="text-center py-3">
                <div class="spinner-border"></div>
                <p class="mt-2">Loading spots...</p>
              </div>
              
              <div v-else-if="lotSpots.length === 0" class="text-center py-3 text-muted">
                <i class="fas fa-car fa-3x mb-3"></i>
                <p>No spots found for this lot</p>
                <button @click="generateSpots" class="btn btn-primary">Generate Spots</button>
              </div>
              
              <div v-else>
                <div class="spots-grid">
                  <div 
                    v-for="spot in lotSpots" 
                    :key="spot.id"
                    class="spot-card"
                    :class="{
                      'available': spot.status === 'A',
                      'occupied': spot.status === 'O'
                    }"
                  >
                    <div class="spot-number">{{ spot.spot_number }}</div>
                    <div class="spot-status">{{ spot.status === 'A' ? 'Available' : 'Occupied' }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'AdminLots',
  data() {
    return {
      loading: false,
      saving: false,
      actionLoading: null,
      generatingSpots: false,
      loadingSpots: false,
      searchQuery: '',
      statusFilter: '',
      sortBy: 'name',
      parkingLots: [],
      selectedLot: null,
      lotSpots: [],
      isEditing: false,
      formError: null,
      lotForm: {
        prime_location_name: '',
        address: '',
        pin_code: '',
        number_of_spots: 0,
        price_per_hour: 0,
        description: '',
        is_active: true
      }
    }
  },
  computed: {
    filteredLots() {
      let filtered = this.parkingLots
      
      // Filter by search query
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(lot => 
          lot.prime_location_name.toLowerCase().includes(query) ||
          lot.address.toLowerCase().includes(query)
        )
      }
      
      // Filter by status
      if (this.statusFilter) {
        const isActive = this.statusFilter === 'active'
        filtered = filtered.filter(lot => lot.is_active === isActive)
      }
      
      // Sort results
      return filtered.sort((a, b) => {
        switch (this.sortBy) {
          case 'spots':
            return b.number_of_spots - a.number_of_spots
          case 'price':
            return a.price_per_hour - b.price_per_hour
          case 'occupancy':
            return this.getOccupancyRate(b) - this.getOccupancyRate(a)
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
    ...mapActions('admin', [
      'fetchAllParkingLots', 
      'createParkingLot', 
      'updateParkingLot', 
      'deleteParkingLot',
      'fetchLotSpots',
      'generateLotSpots'
    ]),
    
    async loadParkingLots() {
      this.loading = true
      try {
        this.parkingLots = await this.fetchAllParkingLots()
      } catch (error) {
        console.error('Error loading parking lots:', error)
        this.$toast?.error('Failed to load parking lots')
      } finally {
        this.loading = false
      }
    },
    
    getOccupancyRate(lot) {
      if (lot.number_of_spots === 0) return 0
      return Math.round((lot.occupied_spots / lot.number_of_spots) * 100)
    },
    
    showCreateModal() {
      this.isEditing = false
      this.lotForm = {
        prime_location_name: '',
        address: '',
        pin_code: '',
        number_of_spots: 0,
        price_per_hour: 0,
        description: '',
        is_active: true
      }
      this.formError = null
      
      const modal = new window.bootstrap.Modal(document.getElementById('lotModal'))
      modal.show()
    },
    
    editLot(lot) {
      this.isEditing = true
      this.lotForm = { ...lot }
      this.formError = null
      
      const modal = new window.bootstrap.Modal(document.getElementById('lotModal'))
      modal.show()
    },
    
    async saveLot() {
      this.formError = null
      this.saving = true
      
      try {
        if (this.isEditing) {
          await this.updateParkingLot({
            id: this.lotForm.id,
            ...this.lotForm
          })
        } else {
          await this.createParkingLot(this.lotForm)
        }
        
        // Hide modal
        const modal = window.bootstrap.Modal.getInstance(document.getElementById('lotModal'))
        modal.hide()
        
        // Reload lots
        await this.loadParkingLots()
        
        this.$toast?.success(`Parking lot ${this.isEditing ? 'updated' : 'created'} successfully!`)
        
      } catch (error) {
        this.formError = error.response?.data?.message || 'Failed to save parking lot'
      } finally {
        this.saving = false
      }
    },
    
    async toggleLotStatus(lot) {
      this.actionLoading = lot.id
      try {
        await this.updateParkingLot({
          id: lot.id,
          is_active: !lot.is_active
        })
        
        await this.loadParkingLots()
        this.$toast?.success(`Parking lot ${lot.is_active ? 'deactivated' : 'activated'} successfully!`)
        
      } catch (error) {
        console.error('Error toggling lot status:', error)
        this.$toast?.error('Failed to update lot status')
      } finally {
        this.actionLoading = null
      }
    },
    
    async deleteLot(lot) {
      if (!confirm(`Are you sure you want to delete "${lot.prime_location_name}"? This action cannot be undone.`)) {
        return
      }
      
      this.actionLoading = lot.id
      try {
        await this.deleteParkingLot(lot.id)
        await this.loadParkingLots()
        this.$toast?.success('Parking lot deleted successfully!')
        
      } catch (error) {
        console.error('Error deleting lot:', error)
        this.$toast?.error('Failed to delete parking lot')
      } finally {
        this.actionLoading = null
      }
    },
    
    async manageLotSpots(lot) {
      this.selectedLot = lot
      this.lotSpots = []
      
      const modal = new window.bootstrap.Modal(document.getElementById('spotsModal'))
      modal.show()
      
      await this.loadLotSpots()
    },
    
    async loadLotSpots() {
      if (!this.selectedLot) return
      
      this.loadingSpots = true
      try {
        this.lotSpots = await this.fetchLotSpots(this.selectedLot.id)
      } catch (error) {
        console.error('Error loading lot spots:', error)
        this.$toast?.error('Failed to load parking spots')
      } finally {
        this.loadingSpots = false
      }
    },
    
    async generateSpots() {
      if (!this.selectedLot) return
      
      this.generatingSpots = true
      try {
        await this.generateLotSpots(this.selectedLot.id)
        await this.loadLotSpots()
        await this.loadParkingLots() // Refresh lot data
        this.$toast?.success('Parking spots generated successfully!')
        
      } catch (error) {
        console.error('Error generating spots:', error)
        this.$toast?.error('Failed to generate parking spots')
      } finally {
        this.generatingSpots = false
      }
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

.progress {
  border-radius: 4px;
}

.modal-content {
  border-radius: 12px;
  border: none;
}

.spots-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
  gap: 10px;
  max-height: 400px;
  overflow-y: auto;
}

.spot-card {
  border: 2px solid #dee2e6;
  border-radius: 8px;
  padding: 10px;
  text-align: center;
  transition: all 0.2s;
}

.spot-card.available {
  border-color: #28a745;
  background-color: #d4edda;
}

.spot-card.occupied {
  border-color: #dc3545;
  background-color: #f8d7da;
}

.spot-number {
  font-weight: bold;
  font-size: 1.1rem;
}

.spot-status {
  font-size: 0.8rem;
  margin-top: 5px;
}
</style>
