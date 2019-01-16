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
    console.log('invalidateSession')
    return new Promise((resolve, reject) => {
      context.commit('removeSession')
      resolve()
    })
  },

  saveState (context) {
    console.log('saveState')
    localStorage.setItem('state', JSON.stringify(state))
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
    state.userData = userData
  },

  setJwtToken (state, token) {
    console.log('setJwtToken payload: ', token)
    state.token = token
  },

  removeSession (state) {
    console.log('removeSession')
    state.token = ''
    state.userData = {}
    state.contracts = []
  },

  loadState (state) {
    console.log('loadState')
    var loadedState = localStorage.getItem('state')
    if (loadedState) {
      this.replaceState(
        Object.assign(state, JSON.parse(loadedState))
      )
    }
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
  },
  currentUser (state) {
    return state.userData.id
  },
  currentUserData (state) {
    return state.userData
  }
}

const store = new Vuex.Store({
  state,
  actions,
  mutations,
  getters
})

store.subscribe((mutation, state) => {
  store.dispatch('saveState')
})

window.store = store

export default store
