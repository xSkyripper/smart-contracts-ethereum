<template>
  <div class="contracts">
    <h1>{{ msg }}</h1>
    <a href="" @click.prevent="contracts">Contracts</a>
  </div>
</template>

<script>
export default {
  name: 'ContractsComponent',
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
    contracts () {
      alert('Contracts')
    }
  }
}
</script>
