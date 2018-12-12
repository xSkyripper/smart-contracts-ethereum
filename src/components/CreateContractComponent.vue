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
              <label for="service">Service</label>
              <div class="input-group">
                <input type="text" class="form-control" id="service" placeholder="Service" required>
                <div class="invalid-feedback" style="width: 100%;">Service is required</div>
              </div>
            </div>

            <div class="mb-3">
              <label for="description">Description
                <span class="text-muted">(Optional)</span>
              </label>
              <input type="text" class="form-control" id="description" placeholder="Description">
              <div class="invalid-feedback">Description is optional</div>
            </div>

            <div class="mb-3">
              <label for="walletId">Amount Due</label>
              <div class="input-group">
                <input type="number" step=".01" class="form-control" id="walletId" required>
                <div class="invalid-feedback" style="width: 100%;">Amount due is required</div>
              </div>
            </div>

            <button class="btn float-right login_btn" type="submit">Create contract</button>
          </form>
        </div>
        <div class="card-footer">
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CreateContractComponent',
  props: {
    msg: String
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
