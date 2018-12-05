<template>
  <div class="col-sm-6 col-md-4 col-lg-3">
    <div class="contract">
      <div class="panel panel-default">
        <div class="panel-heading">
          <h3 class="panel-title">{{ name }}</h3>
        </div>
        <div class="panel-body">
          <img class="img-rounded img-center" :src="picture" data-holder-rendered="true">
          <span class="info-line">
            <strong>Service</strong>:
            <span class="service">{{ service }}</span>
          </span>

          <span class="info-line">
            <strong>Due Date</strong>:
            <span class="due_date">{{ due_date }}</span>
          </span>

          <span class="info-line">
            <strong>Location</strong>:
            <span class="location">{{ location }}</span>
          </span>

          <button class="btn btn-default btn-pay" type="button" data-id="0">Pay</button>
        </div>
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

.contract {
  background-color: rgba(0, 0, 0, 0.8) !important;
  padding: 1.5rem 0;
  margin-bottom: 30px;
  border-radius: 0.3rem;

  .img-rounded {
    width: 200px;
    height: 200px;
    margin-bottom: 1.5rem;
  }

  .info-line {
    display: block;
  }

  .btn-pay {
    margin-top: 1.5rem;
    background-color: #ffc312;
    padding: .35rem 2rem;
  }
}
</style>
