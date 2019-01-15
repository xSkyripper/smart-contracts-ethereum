<template>
  <div class="container" style="min-height:70vh">
    <HelloWorld msg="Welcome to CryptoTax!"/>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'home',
  components: {
    HelloWorld
  }
}
</script>

<style lang="scss">

</style>
