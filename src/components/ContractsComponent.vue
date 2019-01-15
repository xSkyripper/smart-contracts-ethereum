<template>
  <div class="container contracts">
    <h1>{{ msg }}</h1>
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

import ContractComponent from '@/components/ContractComponent.vue'

export default {
  name: 'ContractsComponent',
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
  mounted: function() {
    axios.get("http://localhost:5000/api/users/" + 12 + "/contracts/").then(response => {
        this.contracts = response.data.contracts
    })
  },
  methods: {
  }
}
</script>

<style lang="scss" scoped>
.contracts {
  h1 {
    margin-bottom:30px;
  }

  margin-top:30px;
}
</style>
