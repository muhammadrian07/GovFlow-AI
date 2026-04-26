import axios from 'axios'

/**
 * API service using Axios
 * Handles all backend communication
 * Base URL configured from environment or defaults to localhost
 */

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor
api.interceptors.request.use(
  config => {
    console.log('API Request:', config.method.toUpperCase(), config.url)
    return config
  },
  error => {
    console.error('Request Error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  response => {
    console.log('API Response:', response.status, response.data)
    return response
  },
  error => {
    console.error('Response Error:', error.response?.status, error.response?.data)
    return Promise.reject(error)
  }
)

export default api
