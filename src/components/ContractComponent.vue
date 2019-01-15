<template>
  <div class="col-sm-6 col-md-4 col-lg-3">
    <div class="contract">
      <div class="panel panel-default">
        <div class="panel-heading">
          <h3 class="panel-title">{{ name }}</h3>
        </div>
        <div class="panel-body">
          <img class="img-rounded img-center" src="../assets/ETHEREUM-ICON_Black_small.png" data-holder-rendered="true">
          <span class="info-line">
            <strong>Description</strong>:
            <span class="service">{{ description }}</span>
          </span>

          <span class="info-line">
            <strong>Amount due</strong>:
            <span class="due_date">{{ amount_due | wei_to_eth }} ETH</span>
          </span>

          <button v-if="admin" @click="showOnboardPayerModal" class="btn btn-default btn-pay" type="button" data-id="0">On-board payer</button>
          <button v-else @click="pay" class="btn btn-default btn-pay" type="button" data-id="0">Pay</button>
        </div>
      </div>
    </div>
    <OnboardPayerModalComponent :name="name" :service="description" :id="id" v-show="isOnboardPayerModalVisible" @close="closeOnboardPayerModal"/>
  </div>
</template>
<script>
import OnboardPayerModalComponent from '@/components/OnboardPayerModalComponent.vue'

export default {
  name: 'ContractComponent',
  components: {
    OnboardPayerModalComponent
  },
  props: {
    id: Number,
    name: String,
    picture: String,
    description: String,
    amount_due: Number,
    admin: Boolean
  },
  data () {
    return {
      resources: [],
      error: '',
      isOnboardPayerModalVisible: false }
  },
  methods: {
    pay () {
      alert('Pay')
    },
    onboard () {
      alert('On-board payer')
    },
    showOnboardPayerModal () {
      this.isOnboardPayerModalVisible = true
    },
    closeOnboardPayerModal () {
      this.isOnboardPayerModalVisible = false
    }
  },
  filters: {
    wei_to_eth: function (value) {
      return value / 1000000000000000000
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
