<template>
  <div class="container" style="min-height:68vh">
    <div class="d-flex justify-content-center mb-5">
      <div class="card">
        <div class="card-body mx-4">
          <h1>{{ msg }}</h1>
        </div>
      </div>
    </div>
    <div class="row">
      <ContractComponent
        v-for="r in contracts"
        :key="r.id"
        :id="r.id"
        :name="r.name"
        :picture="r.picture"
        :amount_due="r.amount_due"
        :description="r.description"
        :admin=true
      />
    </div>
  </div>
</template>
<script src="https://cdnjs.cloudflare.com/ajax/libs/vue/1.0.18/vue.min.js"></script>
<script>
import $backend from '../backend'
import Vue from 'vue'

import ContractComponent from '@/components/ContractComponent.vue'

export default {
  name: 'ContractsAdminComponent',
  components: {
    ContractComponent
  },
  props: {
    msg: String
  },
  data () {
    return {
      contracts: [],
      error: ''
    }
  },
  mounted () {
    $backend.fetchAllContracts().then(response => {
      this.contracts = response.data.contracts
    })
  },
  methods: {
  }
}
</script>

<style lang="scss" scoped>
.card {
  background-color: rgba(0, 0, 0, 0.8) !important;
}
</style>
