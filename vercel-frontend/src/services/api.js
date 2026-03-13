import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add request interceptor to include auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Add response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Auth API
export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
  logout: () => api.post('/auth/logout'),
  verifyToken: () => api.get('/auth/verify'),
  refreshToken: () => api.post('/auth/refresh'),
}

// Accounts API
export const accountsAPI = {
  getAccounts: () => api.get('/accounts'),
  getAccount: (id) => api.get(`/accounts/${id}`),
  createAccount: (data) => api.post('/accounts', data),
  updateAccount: (id, data) => api.put(`/accounts/${id}`, data),
  deleteAccount: (id) => api.delete(`/accounts/${id}`),
}

// Challenges API
export const challengesAPI = {
  getChallenges: () => api.get('/challenges'),
  getChallenge: (id) => api.get(`/challenges/${id}`),
  createChallenge: (data) => api.post('/challenges', data),
  updateChallenge: (id, data) => api.put(`/challenges/${id}`, data),
  deleteChallenge: (id) => api.delete(`/challenges/${id}`),
}

// Leaderboard API
export const leaderboardAPI = {
  getLeaderboard: (params) => api.get('/leaderboard', { params }),
  getUserRank: (userId) => api.get(`/leaderboard/user/${userId}`),
}

// Payments API
export const paymentsAPI = {
  getPayments: () => api.get('/payments'),
  getPayment: (id) => api.get(`/payments/${id}`),
  createPayment: (data) => api.post('/payments', data),
  updatePayment: (id, data) => api.put(`/payments/${id}`, data),
}

// Admin API
export const adminAPI = {
  getUsers: (params) => api.get('/admin/users', { params }),
  getUser: (id) => api.get(`/admin/users/${id}`),
  updateUser: (id, data) => api.put(`/admin/users/${id}`, data),
  deleteUser: (id) => api.delete(`/admin/users/${id}`),
  
  getAdminAccounts: (params) => api.get('/admin/accounts', { params }),
  getAdminAccount: (id) => api.get(`/admin/accounts/${id}`),
  updateAdminAccount: (id, data) => api.put(`/admin/accounts/${id}`, data),
  
  getAdminPayments: (params) => api.get('/admin/payments', { params }),
  getAdminPayment: (id) => api.get(`/admin/payments/${id}`),
  
  getAdminChallenges: (params) => api.get('/admin/challenges', { params }),
  updateAdminChallenge: (id, data) => api.put(`/admin/challenges/${id}`, data),
  
  getAnalytics: (params) => api.get('/admin/analytics', { params }),
  getRiskMonitor: () => api.get('/admin/risk-monitor'),
  getViolations: (params) => api.get('/admin/violations', { params }),
  updateViolation: (id, data) => api.put(`/admin/violations/${id}`, data),
}

export default api
