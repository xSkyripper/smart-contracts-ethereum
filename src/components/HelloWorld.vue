<template>
  <div class="d-flex justify-content-center">
    <div class="card">
      <div class="card-body mx-4">
          <h1>{{ msg }}</h1>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}

.card {
  margin-top: auto;
  margin-bottom: auto;
  background-color: rgba(0, 0, 0, 0.6) !important;
}
</style>
