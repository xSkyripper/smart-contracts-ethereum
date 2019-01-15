import Vue from 'vue'
import Vuex from 'vuex'
import $backend from './backend'

Vue.use(Vuex)

const state = {
  loggedIn: false,
  jwt: null,
  userData: {
    userId: null,
    ethereumId: null,
    isAdmin: false
  },
  contracts: []
}

const actions = {
  loadUserContracts (context) {
    return $backend.fetchUserContracts(state.userData.userId)
      .then((response) => context.commit('setUserContracts', { contracts: response }))
  }
}

const mutations = {
  setUserContracts (state, payload) {
    state.contracts = payload.contracts
  }
}

const getters = {
}

export default new Vuex.Store({
  state,
  actions,
  mutations,
  getters
})
