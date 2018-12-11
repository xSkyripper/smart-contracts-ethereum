<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/login">Login</router-link> |
      <router-link to="/register">Register</router-link> |
      <router-link to="/contracts">Contracts</router-link> |
      <router-link to="/contracts/admin">Contracts (Admin)</router-link> |
      <router-link to="/contracts/new">New Contract (Admin)</router-link>
    </div>
    <router-view/>

  </div>
</template>

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

</style>
