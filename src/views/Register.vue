<template>
    <div class="register">
        <a href="" @click.prevent="register">Register</a>
    </div>
</template>

<script>

export default {
  name: 'register',
  data () {
    return {
      resources: [],
      error: ''
    }
  },
  methods: {
    register () {
      alert('Register')
    }
  }
}

</script>

<style lang="scss">
</style>
