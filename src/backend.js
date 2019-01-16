import axios from 'axios'
import store from './store'

let $axios = axios.create({
  baseURL: 'http://localhost:5000/',
  timeout: 5000,
  headers: {'Content-Type': 'application/x-www-form-urlencoded'}
})

// Request Interceptor
$axios.interceptors.request.use(function (config) {
  config.headers['Authorization'] = 'Bearer ' + store.getters.getJwtToken
  console.log(config.headers['Authorization'])
  return config
})

// Response Interceptor to handle and log errors
$axios.interceptors.response.use(function (response) {
  return response
}, function (error) {
  // Handle Error
  console.log(error)
  return Promise.reject(error)
})

export default {
  register (authorizationParameters) {
    return $axios.post('register', authorizationParameters)
      .then(response => response)
  },

  login (authorizationParameters) {
    return $axios.post('login', authorizationParameters)
      .then(response => response)
  },

  fetchUserContracts () {
    const userId = store.getters.currentUser
    return $axios.get(`api/users/${userId}/contracts`).then()
  },

  fetchAllContracts () {
    return $axios.get('api/contracts').then()
  },

  onboard (payer) {
    const config = {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    }

    return axios.post('http://localhost:5000/onboard', payer, config)
      .then(response => response)
  },

  addContract (info) {
    const config = {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    }

    return $axios.post('http://localhost:5000/api/contracts', info, config)
      .then(response => response)
  }
}
