import { createStore } from 'vuex'
import authModule from './modules/auth'
import parkingModule from './modules/parking'
import adminModule from './modules/admin'

export default createStore({
  state: {
    isLoading: false,
    alertMessage: '',
    alertType: 'info'
  },
  
  mutations: {
    SET_LOADING(state, loading) {
      state.isLoading = loading
    },
    
    SET_ALERT(state, { message, type = 'info' }) {
      state.alertMessage = message
      state.alertType = type
    },
    
    CLEAR_ALERT(state) {
      state.alertMessage = ''
      state.alertType = 'info'
    }
  },
  
  actions: {
    setLoading({ commit }, loading) {
      commit('SET_LOADING', loading)
    },
    
    showAlert({ commit }, { message, type = 'info' }) {
      commit('SET_ALERT', { message, type })
      
      // Auto-clear alert after 5 seconds
      setTimeout(() => {
        commit('CLEAR_ALERT')
      }, 5000)
    },
    
    clearAlert({ commit }) {
      commit('CLEAR_ALERT')
    }
  },
  
  modules: {
    auth: authModule,
    parking: parkingModule,
    admin: adminModule
  }
})
