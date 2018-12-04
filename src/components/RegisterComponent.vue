<template>
    <div class="container register">
      <div class="text-center mt-4">
          <h2>{{ msg }}</h2>
      </div>
      <div class="row d-flex justify-content-center">
        <div class="column mb-6 mt-4">
          <form class="needs-validation" novalidate>
            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="firstName">First name</label>
                <input type="text" class="form-control" id="firstName" placeholder="" value="" required>
                <div class="invalid-feedback">
                  Valid first name is required.
                </div>
              </div>
              <div class="col-md-6 mb-3">
                <label for="lastName">Last name</label>
                <input type="text" class="form-control" id="lastName" placeholder="" value="" required>
                <div class="invalid-feedback">
                  Valid last name is required.
                </div>
              </div>
            </div>

            <div class="mb-3">
              <label for="username">Username</label>
              <div class="input-group">
                <div class="input-group-prepend">
                  <span class="input-group-text">@</span>
                </div>
                <input type="text" class="form-control" id="username" placeholder="Username" required>
                <div class="invalid-feedback" style="width: 100%;">
                  Your username is required.
                </div>
              </div>
            </div>

            <div class="mb-3">
              <label for="email">Email <span class="text-muted">(Optional)</span></label>
              <input type="email" class="form-control" id="email" placeholder="you@example.com">
              <div class="invalid-feedback">
                Please enter a valid email address for shipping updates.
              </div>
            </div>

            <div class="mb-3">
              <label for="username">Ethereum Wallet ID</label>
              <div class="input-group">
                <input type="text" class="form-control" id="walletId" placeholder="0x...." required>
                <div class="invalid-feedback" style="width: 100%;">
                  Your Wallet ID is required.
                </div>
              </div>
            </div>

                    <button class="btn btn-primary btn-lg btn-block mt-5" type="submit">Register</button>
          </form>
        </div>
      </div>

      <footer class="my-5 pt-5 text-muted text-center text-small">
        <p class="mb-1">&copy; 2018-2019 SmartContracts</p>
      </footer>
  </div>
</template>

<script>
export default {
  name: 'RegisterComponent',
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
