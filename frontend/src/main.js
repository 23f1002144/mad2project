import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

// Bootstrap CSS
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

// FontAwesome Icons
import '@fortawesome/fontawesome-free/css/all.min.css'

// Custom CSS
import './assets/css/main.css'

const app = createApp(App)

app.use(store)
app.use(router)

// Global error handler
app.config.errorHandler = (error, instance, info) => {
  console.error('Global error:', error)
  console.error('Component info:', info)
}

app.mount('#app')
