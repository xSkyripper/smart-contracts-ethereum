<template>
  <div class="container login">
    <div class="d-flex justify-content-center h-100">
      <div class="card">
        <div class="card-header">
          <h3>Register</h3>
        </div>
        <div class="card-body">
          <form class="needs-validation" novalidate>
            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="firstName">First name</label>
                <input  v-model="user.first_name"  type="text" class="form-control" id="firstName" placeholder value required>
                <div class="invalid-feedback">Valid first name is required.</div>
              </div>
              <div class="col-md-6 mb-3">
                <label for="lastName">Last name</label>
                <input v-model="user.last_name" type="text" class="form-control" id="lastName" placeholder value required>
                <div class="invalid-feedback">Valid last name is required.</div>
              </div>
            </div>

            <div class="mb-3">
              <label for="password">Password</label>
              <div class="input-group">
                <div class="input-group-prepend">
                  <span class="input-group-text">🗝</span>
                </div>
                <input v-model="user.password" type="password" class="form-control" id="password" placeholder="Password" required>
                <div class="invalid-feedback" style="width: 100%;">Your password is required.</div>
              </div>
            </div>

            <div class="mb-3">
              <label for="email">Email
                <span class="text-muted">(Optional)</span>
              </label>
              <input v-model="user.email" type="email" class="form-control" id="email" placeholder="you@example.com">
              <div class="invalid-feedback">Please enter a valid email address for shipping updates.</div>
            </div>

            <div class="mb-3">
              <label for="walletId">Ethereum Wallet ID</label>
              <div class="input-group">
                <input v-model="user.ethereum_id" type="text" class="form-control" id="walletId" placeholder="0x...." required>
                <div class="invalid-feedback" style="width: 100%;">Your Wallet ID is required.</div>
              </div>
            </div>

            <div class="mb-3">
              <label for="govId">Gov ID</label>
              <div class="input-group">
                <input v-model="user.gov_id" type="text" class="form-control" id="govId" placeholder="0x...." required>
                <div class="invalid-feedback" style="width: 100%;">Your Wallet ID is required.</div>
              </div>
            </div>

            <div class="form-group">
              <input
                type="submit"
                value="Register"
                class="btn float-right login_btn"
                @click.prevent="register"
              >
            </div>
          </form>
        </div>
        <div class="card-footer">
          <div class="d-flex justify-content-center links">Already have an account?
            <router-link to="/login">Login</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import qs from 'qs'

export default {
  name: 'RegisterComponent',
  props: {
    msg: String
  },
  data () {
    return {
      user: {
        first_name: '',
        last_name: '',
        password: '',
        email: '',
        ethereum_id: '',
        gov_id: ''
      }
    }
  },
  methods: {
    register () {
      const config = {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      }

      return axios.post('http://localhost:5000/register', qs.stringify(this.user), config)
        .then(response => {
          console.log(response)
        })
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
  height: 670px;
  margin-top: auto;
  margin-bottom: auto;
  width: 35%;
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
  width: 100px;
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
