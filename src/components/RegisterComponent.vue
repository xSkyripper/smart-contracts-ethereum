<template>
  <div class="register">
    <h1>{{ msg }}</h1>
    <a href="" @click.prevent="register">Register</a>
  </div>
</template>

<script>
export default {
  name: 'RegisterComponent',
  props: {
    msg: String
  },
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
