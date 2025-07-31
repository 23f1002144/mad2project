import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'

// Public views
import Home from '@/views/Home.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'

// User views
import UserDashboard from '@/views/user/Dashboard.vue'
import ParkingLots from '@/views/user/ParkingLots.vue'
import UserProfile from '@/views/user/Profile.vue'
import UserReservations from '@/views/user/Reservations.vue'

// Admin views
import AdminDashboard from '@/views/admin/Dashboard.vue'
import AdminLots from '@/views/admin/Lots.vue'
import AdminUsers from '@/views/admin/Users.vue'
import AdminReservations from '@/views/admin/Reservations.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: false }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false, guestOnly: true }
  },
  {
    path: '/register',
    name: 'Register', 
    component: Register,
    meta: { requiresAuth: false, guestOnly: true }
  },
  
  // User routes
  {
    path: '/dashboard',
    name: 'UserDashboard',
    component: UserDashboard,
    meta: { requiresAuth: true, userType: 'user' }
  },
  {
    path: '/parking-lots',
    name: 'ParkingLots',
    component: ParkingLots,
    meta: { requiresAuth: true, userType: 'user' }
  },
  {
    path: '/profile',
    name: 'UserProfile',
    component: UserProfile,
    meta: { requiresAuth: true, userType: 'user' }
  },
  {
    path: '/reservations',
    name: 'UserReservations', 
    component: UserReservations,
    meta: { requiresAuth: true, userType: 'user' }
  },
  
  // Admin routes
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, userType: 'admin' }
  },
  {
    path: '/admin/lots',
    name: 'AdminLots',
    component: AdminLots,
    meta: { requiresAuth: true, userType: 'admin' }
  },
  {
    path: '/admin/users',
    name: 'AdminUsers',
    component: AdminUsers,
    meta: { requiresAuth: true, userType: 'admin' }
  },
  {
    path: '/admin/reservations',
    name: 'AdminReservations',
    component: AdminReservations,
    meta: { requiresAuth: true, userType: 'admin' }
  },
  
  // 404 page
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// Navigation guards
router.beforeEach((to, from, next) => {
  const isAuthenticated = store.getters.isAuthenticated
  const userType = store.getters.userType
  
  // Check if route requires authentication
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
    return
  }
  
  // Check if route is for guests only
  if (to.meta.guestOnly && isAuthenticated) {
    const dashboardRoute = userType === 'admin' ? '/admin/dashboard' : '/dashboard'
    next(dashboardRoute)
    return
  }
  
  // Check user type permissions
  if (to.meta.userType && to.meta.userType !== userType) {
    // Redirect to appropriate dashboard
    const dashboardRoute = userType === 'admin' ? '/admin/dashboard' : '/dashboard'
    next(dashboardRoute)
    return
  }
  
  next()
})

export default router
