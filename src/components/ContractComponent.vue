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

          <button v-if="admin" @click="showOnboardPayerModal" class="btn btn-default btn-pay" type="button" data-id="0">On-board payer</button>
          <button v-else @click="showPayContractModal" class="btn btn-default btn-pay" type="button" data-id="0">Pay</button>
        </div>
      </div>
    </div>
    <OnboardPayerModalComponent :name="name" :service="service" v-show="isOnboardPayerModalVisible" @close="closeOnboardPayerModal"/>
    <PayContractModalComponent :name="name" :service="service" v-show="isPayContractModalVisible" @close="closePayContractModal"/>
  </div>

</template>

<script>
import OnboardPayerModalComponent from '@/components/OnboardPayerModalComponent.vue'
import PayContractModalComponent from '@/components/PayContractModalComponent.vue'

export default {
  name: 'ContractComponent',
  components: {
    OnboardPayerModalComponent,
    PayContractModalComponent
  },
  props: {
    name: String,
    picture: String,
    service: String,
    due_date: String,
    location: String,
    admin: Boolean
  },
  data () {
    return {
      resources: [],
      error: '',
      isOnboardPayerModalVisible: false,
      isPayContractModalVisible: false
    }
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
    },
    showPayContractModal () {
      this.isPayContractModalVisible = true
    },
    closePayContractModal () {
      this.isPayContractModalVisible = false
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
