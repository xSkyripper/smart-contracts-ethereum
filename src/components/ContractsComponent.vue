<template>
  <div class="container contracts" style="min-height:68vh">
    <div class="d-flex justify-content-center">
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
        :admin=false
      />
    </div>
  </div>
</template>
<script src="https://cdnjs.cloudflare.com/ajax/libs/vue/1.0.18/vue.min.js"></script>
<script>
import axios from 'axios'
import Vue from 'vue'
import { mapState } from 'vuex'

import ContractComponent from '@/components/ContractComponent.vue'

export default {
  name: 'ContractsComponent',
  components: {
    ContractComponent
  },
  props: {
    msg: String
  },
  // computed: mapState({
  //   contracts: state => state.contracts
  // }),
  data () {
    return {
      contracts: [],
      error: ''
    }
  },
  mounted: function() {
    axios.get("http://localhost:5000/api/users/" + 12 + "/contracts/").then(response => {
        this.contracts = response.data.contracts
    })
  },
  // beforeMount () {
  //   this.$store.dispatch('loadUserContracts')
  // }
}
</script>

<style lang="scss" scoped>
.contracts {
  margin-top:30px;
}
.card {
  background-color: rgba(0, 0, 0, 0.6) !important;
}
</style>
