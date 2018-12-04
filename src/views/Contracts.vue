<template>
    <div class="contracts">
        <a href="" @click.prevent="contracts">Contracts</a>
    </div>
</template>

<script>

export default {
  name: 'contracts',
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

<style lang="scss">
</style>
