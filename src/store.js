import Vue from 'vue'
import Vuex from 'vuex'
import qs from 'qs'
import $backend from './backend'
import { isValidJwt, EventBus } from './utils'

Vue.use(Vuex)

const state = {
  token: '',
  userData: {},
  contracts: []
}

const actions = {
  loadUserContracts (context) {
    return $backend.fetchUserContracts(state.userData.userId)
      .then((response) => context.commit('setUserContracts', { contracts: response }))
  },

  login (context, userData) {
    return $backend.login(qs.stringify(userData))
      .then(response => {
        context.commit('setJwtToken', response.data.access_token)
        context.commit('setUserData', response.data.user_data)
      })
      .catch(error => {
        console.log('Error on login: ', error)
        EventBus.$emit('failedLogin: ', error)
      })
  },

  invalidateSession (context) {
    return new Promise((resolve, reject) => {
      context.commit('removeSession')
      resolve()
    })
  }

  // register (context, userData) {
  //   // context.commit('setUserData', { userData })
  //   return $backend.register(userData)
  //     .then(context.dispatch('login', userData))
  //     .catch(error => {
  //       console.log('Error on register: ', error)
  //       EventBus.$emit('failedRegister: ', error)
  //     })
  // }
}

const mutations = {
  setUserContracts (state, payload) {
    state.contracts = payload.contracts
  },

  setUserData (state, userData) {
    console.log('setUserData payload: ', userData)
    localStorage.setItem('userData', userData)
    state.userData = userData
  },

  setJwtToken (state, token) {
    console.log('setJwtToken payload: ', token)
    localStorage.setItem('token', token)
    state.token = token
  },

  removeSession (state) {
    console.log('removeSession')
    state.token = ''
    state.userData = {}
    state.contracts = []
  }

  // TODO: retrieve cache from localStorage on init
}

const getters = {
  isAuthenticated (state) {
    return isValidJwt(state.token)
  },
  isAdmin (state) {
    return state.userData.is_admin
  },
  getJwtToken (state) {
    return state.token
  }
}

const store = new Vuex.Store({
  state,
  actions,
  mutations,
  getters
})

window.store = store

export default store
