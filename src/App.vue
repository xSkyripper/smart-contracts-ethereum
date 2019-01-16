<template>
  <div id="app">
    <div id="nav" class="py-3 mb-5" style="background-color: rgba(0, 0, 0, 0.8) !important;">
      <router-link class="mx-1" to="/">
        Home
      </router-link> |
      <router-link class="mx-1" to="/login" v-if="!isAuthenticated">
        Login
      </router-link> |
      <router-link class="mx-1" to="/register" v-if="!isAuthenticated">
        Register
      </router-link> |
      <router-link class="mx-1" to="/contracts" v-if="isAuthenticated && !isAdmin">
        Your contracts
      </router-link> |
      <router-link class="mx-1" to="/contracts/admin" v-if="isAuthenticated && isAdmin">
        All contracts
      </router-link> |
      <router-link class="mx-1" to="/contracts/new" v-if="isAuthenticated && isAdmin">
        New contract
      </router-link>
      <a href="#" @click.prevent="logout" v-if="isAuthenticated">Logout</a>
    </div>
    <router-view/>

  </div>
</template>

<script>
export default {
  computed: {
    isAuthenticated () {
      return this.$store.getters.isAuthenticated
    },
    isAdmin () {
      return this.$store.getters.isAdmin
    }
  },
  methods: {
    logout () {
      console.log('logout')
      this.$store.dispatch('invalidateSession').then(() => {
        this.$router.push('/login')
      })
    }
  }
}

</script>

<style lang="scss">

html,body{
//background-image: url('./assets/544750.jpg');
background-image: url('./assets/eth4.jpg');
background-size: cover;
background-repeat: no-repeat;
background-attachment: fixed;
height: 100%;
font-family: 'Numans', sans-serif;
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: white;
}
#nav {
  padding: 30px;
  a {
    font-weight: bold;
    color: white;
    &.router-link-exact-active {
      color: #ffc312;
    }
  }
}
#plus {
  padding: 0 20px 0 20px;
  display: inline-block;
  font-size: 50px;
  vertical-align: top;
  line-height: 100px;
}
.container {
  height: 100%;
  align-content: center;
}

</style>
