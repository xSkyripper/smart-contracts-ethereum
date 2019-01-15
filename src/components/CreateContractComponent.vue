<template>
  <div class="container login">
    <div class="d-flex justify-content-center h-100">
      <div class="card">
        <div class="card-header">
          <h3>{{ msg }}</h3>
        </div>
        <div class="card-body">
          <form class="needs-validation" novalidate>
            <div class="mb-3">
              <label for="company">Company Name</label>
              <div class="input-group">
                <input
                  type="text"
                  class="form-control"
                  id="company"
                  placeholder="Fictional Company Name"
                  required
                  disabled
                >
                <div class="invalid-feedback" style="width: 100%;">Company name is required</div>
              </div>
            </div>

            <div class="mb-3">
              <label for="name">Name</label>
              <div class="input-group">
                <input v-model="contract.name" type="text" class="form-control" id="name" placeholder="name" required>
                <div class="invalid-feedback" style="width: 100%;">Name is required</div>
              </div>
            </div>

            <div class="mb-3">
              <label for="description">Description
                <span class="text-muted">(Optional)</span>
              </label>
              <input v-model="contract.description" type="text" class="form-control" id="description" placeholder="Description">
              <div class="invalid-feedback">Description is optional</div>
            </div>

            <div class="mb-3">
              <label for="walletId">Amount Due</label>
              <div class="input-group">
                <input v-model="contract.amount_due" type="number" step="10000" class="form-control" id="amount_dueamount_due" required>
                <div class="invalid-feedback" style="width: 100%;">Amount due is required</div>
              </div>
            </div>

            <div class="form-group">
              <input
                type="submit"
                value="Create contract"
                class="btn float-right login_btn"
                @click.prevent="addContract"
              >
            </div>
          </form>
        </div>
        <div class="card-footer">
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import qs from 'qs'
import $backend from '../backend'

export default {
  name: 'CreateContractComponent',
  props: {
    msg: String
  },
  data () {
    return {
      contract: {
        name: '',
        description: '',
        amount_due: ''
      }
    }
  },
  methods: {
    addContract () {
      $backend.addContract(qs.stringify(this.contract))
          .then(response => {
            console.log(response)
      });    
    }
  }
}
</script>

<style lang="scss" scoped>

@import url("https://fonts.googleapis.com/css?family=Numans");

.container {
  height: 100%;
  align-content: center;
}

.card {
  height: 570px;
  margin-top: auto;
  margin-bottom: auto;
  width: 40%;
  background-color: rgba(0, 0, 0, 0.8) !important;
}

.social_icon span {
  font-size: 60px;
  margin-left: 10px;
  color: #ffc312;
}

.social_icon span:hover {
  color: white;
  cursor: pointer;
}

.card-header h3 {
  color: white;
}

label {
  color: white;
}

.social_icon {
  position: absolute;
  right: 20px;
  top: -45px;
}

.input-group-prepend span {
  width: 50px;
  background-color: #ffc312;
  color: black;
  border: 0 !important;
}

input:focus {
  outline: 0 0 0 0 !important;
  box-shadow: 0 0 0 0 !important;
}

.remember {
  color: white;
}

.remember input {
  width: 20px;
  height: 20px;
  margin-left: 15px;
  margin-right: 5px;
}

.login_btn {
  color: black;
  background-color: #ffc312;
  width: 150px;
}

.login_btn:hover {
  color: black;
  background-color: white;
}

.links {
  color: white;
}

.links a {
  margin-left: 4px;
}
</style>
