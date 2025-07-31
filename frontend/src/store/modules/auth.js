import api from '@/services/api'

export default {
  state: {
    token: localStorage.getItem('token'),
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    userType: localStorage.getItem('userType')
  },
  
  mutations: {
    SET_AUTH(state, { token, user, userType }) {
      state.token = token
      state.user = user
      state.userType = userType
      
      // Store in localStorage
      localStorage.setItem('token', token)
      localStorage.setItem('user', JSON.stringify(user))
      localStorage.setItem('userType', userType)
      
      // Set default authorization header
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`
    },
    
    CLEAR_AUTH(state) {
      state.token = null
      state.user = null
      state.userType = null
      
      // Clear localStorage
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      localStorage.removeItem('userType')
      
      // Remove authorization header
      delete api.defaults.headers.common['Authorization']
    },
    
    UPDATE_USER(state, user) {
      state.user = user
      localStorage.setItem('user', JSON.stringify(user))
    }
  },
  
  actions: {
    async login({ commit, dispatch }, { username, password, userType }) {
      try {
        dispatch('setLoading', true, { root: true })
        
        const response = await api.post('/auth/login', {
          username,
          password,
          user_type: userType
        })
        
        const { access_token, user, user_type } = response.data
        
        commit('SET_AUTH', {
          token: access_token,
          user,
          userType: user_type
        })
        
        dispatch('showAlert', {
          message: 'Login successful!',
          type: 'success'
        }, { root: true })
        
        return response.data
      } catch (error) {
        const message = error.response?.data?.error || 'Login failed'
        dispatch('showAlert', {
          message,
          type: 'danger'
        }, { root: true })
        throw error
      } finally {
        dispatch('setLoading', false, { root: true })
      }
    },
    
    async register({ commit, dispatch }, userData) {
      try {
        dispatch('setLoading', true, { root: true })
        
        const response = await api.post('/auth/register', userData)
        
        const { access_token, user, user_type } = response.data
        
        commit('SET_AUTH', {
          token: access_token,
          user,
          userType: user_type
        })
        
        dispatch('showAlert', {
          message: 'Registration successful!',
          type: 'success'
        }, { root: true })
        
        return response.data
      } catch (error) {
        const message = error.response?.data?.error || 'Registration failed'
        dispatch('showAlert', {
          message,
          type: 'danger'
        }, { root: true })
        throw error
      } finally {
        dispatch('setLoading', false, { root: true })
      }
    },
    
    async logout({ commit, dispatch }) {
      commit('CLEAR_AUTH')
      dispatch('showAlert', {
        message: 'Logged out successfully',
        type: 'info'
      }, { root: true })
    },
    
    async checkAuth({ commit, state, dispatch }) {
      if (state.token) {
        try {
          // Set authorization header
          api.defaults.headers.common['Authorization'] = `Bearer ${state.token}`
          
          // Verify token with server
          const response = await api.get('/auth/me')
          
          commit('UPDATE_USER', response.data.user)
        } catch (error) {
          // Token is invalid, clear auth
          commit('CLEAR_AUTH')
        }
      }
    },
    
    async updateProfile({ commit, dispatch }, userData) {
      try {
        dispatch('setLoading', true, { root: true })
        
        const response = await api.put('/user/profile', userData)
        
        commit('UPDATE_USER', response.data.user)
        
        dispatch('showAlert', {
          message: 'Profile updated successfully!',
          type: 'success'
        }, { root: true })
        
        return response.data
      } catch (error) {
        const message = error.response?.data?.error || 'Profile update failed'
        dispatch('showAlert', {
          message,
          type: 'danger'
        }, { root: true })
        throw error
      } finally {
        dispatch('setLoading', false, { root: true })
      }
    },
    
    async changePassword({ dispatch }, { oldPassword, newPassword }) {
      try {
        dispatch('setLoading', true, { root: true })
        
        await api.post('/auth/change-password', {
          old_password: oldPassword,
          new_password: newPassword
        })
        
        dispatch('showAlert', {
          message: 'Password changed successfully!',
          type: 'success'
        }, { root: true })
        
      } catch (error) {
        const message = error.response?.data?.error || 'Password change failed'
        dispatch('showAlert', {
          message,
          type: 'danger'
        }, { root: true })
        throw error
      } finally {
        dispatch('setLoading', false, { root: true })
      }
    }
  },
  
  getters: {
    isAuthenticated: state => !!state.token,
    currentUser: state => state.user,
    userType: state => state.userType,
    isAdmin: state => state.userType === 'admin',
    isUser: state => state.userType === 'user'
  }
}
