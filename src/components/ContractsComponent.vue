<template>
  <div class="container contracts">
    <h1>{{ msg }}</h1>
    <div class="row">
      <ContractComponent
        v-for="r in resources"
        :key="r.id"
        :id="r.id"
        :name="r.description.slice(0,5)"
        :picture="r.picture"
        :due_date="r.tax"
        :service="r.service"

        :admin=$route.meta.admin
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
      resources: [],
      error: ''
    }
  },
  mounted: function() {
    console.log(this.$route.meta.admin)
    if(this.$route.meta.admin) {
      axios.get("http://localhost:5000/api/contracts")
      .then(response => {
        this.resources = response.data.contracts})
    } else {
      axios.get("http://localhost:5000/api/users/" + Vue.prototype.$username + "/contracts/")
      .then(response => {
        this.resources = response.data.contracts})
    }
  },
  methods: {
    contracts () {
      alert('Contracts')
    }
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
