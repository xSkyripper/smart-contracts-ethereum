import axios from 'axios'

let $axios = axios.create({
  baseURL: 'http://localhost:5000/',
  timeout: 5000,
  headers: {'Content-Type': 'application/x-www-form-urlencoded'}
})

// Request Interceptor
$axios.interceptors.request.use(function (config) {
  config.headers['Authorization'] = 'Fake Token'
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

  fetchUserContracts (userId) {
    // return $axios.get(`api/users/{userId}/contracts`).then()
    console.log(`fetchUserContracts for ${userId}`)
    return new Promise((resolve, reject) => {
      const contracts = [
        {
          id: 1,
          name: 'Contract 1',
          picture: 'someLink',
          amount_due: 232323,
          description: 'Description 1'
        },
        {
          id: 2,
          name: 'Contract 2',
          picture: 'someLink 2',
          amount_due: 2323232,
          description: 'Description 2'
        }
      ]
      resolve(contracts)
    })
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

  addContract(info) {
    const config = {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    }

    return $axios.post('http://localhost:5000/api/contracts', info, config)
      .then(response => response)
  }
}
