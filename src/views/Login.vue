<template>
    <div class="login">
        <a href="" @click.prevent="login">Login</a>
    </div>
</template>

<script>

export default {
  name: 'login',
  data () {
    return {
      resources: [],
      error: ''
    }
  },
  methods: {
    login () {
      alert('Login')
    }
  }
}

</script>

<style lang="scss">
</style>
