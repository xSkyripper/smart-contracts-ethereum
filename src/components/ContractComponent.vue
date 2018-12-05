<template>
  <div class="col-sm-6 col-md-4 col-lg-3">
    <div class="panel panel-default">
      <div class="panel-heading">
        <h3 class="panel-title">{{ name }}</h3>
      </div>
      <div class="panel-body">
        <img class="img-rounded img-center" :src="picture" data-holder-rendered="true">
        <br>
        <br>
        <strong>Service</strong>:
        <span class="service">{{ service }}</span>
        <br>
        <strong>Due Date</strong>:
        <span class="due_date">{{ due_date }}</span>
        <br>
        <strong>Location</strong>:
        <span class="location">{{ location }}</span>
        <br>
        <br>
        <button class="btn btn-default btn-pay" type="button" data-id="0">Pay</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ContractComponent',
  props: {
    name: String,
    picture: String,
    service: String,
    due_date: String,
    location: String
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

<style lang="scss" scoped>
.img-rounded {
  width: 200px;
  height: 200px;
}
</style>
