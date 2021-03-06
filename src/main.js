import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import './filters'

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App),
  beforeCreate () {
    this.$store.commit('loadState')
  }
}).$mount('#app')

router.beforeEach((to, from, next) => {
  document.title = to.meta.title
  next()
})
