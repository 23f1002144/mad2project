import axios from 'axios'

// Create axios instance with base configuration
const api = axios.create({
    baseURL: process.env.VUE_APP_API_URL || 'http://localhost:5001/api',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json'
    }
})

// Request interceptor to add auth token
api.interceptors.request.use(
    config => {
        const token = localStorage.getItem('token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    error => {
        return Promise.reject(error)
    }
)

// Response interceptor to handle errors
api.interceptors.response.use(
    response => {
        return response
    },
    error => {
        // Handle common errors
        if (error.response) {
            const status = error.response.status

            switch (status) {
                case 401:
                    // Unauthorized - clear auth and redirect to login
                    localStorage.removeItem('token')
                    localStorage.removeItem('user')
                    localStorage.removeItem('userType')

                    // Only redirect if not already on login page
                    if (window.location.pathname !== '/login') {
                        window.location.href = '/login'
                    }
                    break

                case 403:
                    // Forbidden - show error message
                    console.error('Access forbidden')
                    break

                case 404:
                    // Not found
                    console.error('Resource not found')
                    break

                case 500:
                    // Server error
                    console.error('Server error')
                    break

                default:
                    console.error('API Error:', error.response.data)
            }
        } else if (error.request) {
            // Network error
            console.error('Network error:', error.request)
        } else {
            // Other error
            console.error('Error:', error.message)
        }

        return Promise.reject(error)
    }
)

export default api
