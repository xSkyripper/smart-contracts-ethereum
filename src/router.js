import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Login from './views/Login.vue'
import Register from './views/Register.vue'
import Contracts from './views/Contracts.vue'
import ContractsAdmin from './views/ContractsAdmin.vue'
import NewContract from './views/NewContract.vue'
import Api from './views/Api.vue'
import store from './store'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
      meta: {
        title: 'Home'
      }
    },
    {
      path: '/api',
      name: 'api',
      component: Api,
      meta: {
        title: 'Api'
      }
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta: {
        title: 'Login'
      }
    },
    {
      path: '/register',
      name: 'register',
      component: Register,
      meta: {
        title: 'Register'
      }
    },
    {
      path: '/contracts/admin',
      name: 'admin_contracts',
      component: ContractsAdmin,
      meta: {
        title: 'Contracts',
        admin: true
      }
    },
    {
      path: '/contracts',
      name: 'contracts',
      component: Contracts,
      meta: {
        title: 'Contracts',
        admin: false
      },
      beforeEnter (to, from, next) {
        if (!store.getters.isAuthenticated) {
          next('/login')
        } else {
          next()
        }
      }
    },
    {
      path: '/contracts/new',
      name: 'new_contract',
      component: NewContract,
      meta: {
        title: 'Create Contract',
        admin: true
      }
    }
  ]
})
