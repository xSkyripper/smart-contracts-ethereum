<template>
  <transition name="modal-fade">
    <div class="modal-backdrop">
      <div
        class="modal"
        role="dialog"
        aria-labelledby="modalTitle"
        aria-describedby="modalDescription"
      >
        <header class="modal-header" id="modalTitle">
          <slot name="header">
            <h3 style="text-align: center">{{ name }} - {{ service }}</h3>
            <button type="button" class="btn-close" @click="close" aria-label="Close modal">
              <i class="fa fa-times"></i>
            </button>
          </slot>
        </header>
        <section class="modal-body" id="modalDescription">
          <form>
            <div class="input-group form-group">
              <div class="input-group-prepend">
                <span class="input-group-text">
                  <i class="fas fa-user"></i>
                </span>
              </div>
              <input v-model="payer.gov_id" type="text" class="form-control" placeholder="Social Security Number">
            </div>
            <div class="input-group form-group">
              <div class="input-group-prepend">
                <span class="input-group-text">
                  <i class="far fa-address-card"></i>
                </span>
              </div>
              <input v-model="payer.user_ethereum_id" type="text" class="form-control" placeholder="ETH Wallet ID">
            </div>
          </form>
        </section>
        <footer class="modal-footer">
          <slot name="footer">
            <button
              type="button"
              class="btn btn-primary"
              @click="onboard"
              aria-label="Onboard"
            >Onboard!</button>
          </slot>
        </footer>
      </div>
    </div>
  </transition>
</template>
<script>
import axios from 'axios'
import Vue from 'vue'
import qs from 'qs'
export default {
  name: 'OnboardPayerModalComponent',
  data () {
    return {
      payer: {
        gov_id: '',
        user_ethereum_id: '',
        contract_id: this.id
      }
    }
  },
  methods: {
    close () {
      this.$emit('close')
    },
    onboard () {
      console.log(this.payer.gov_id)
      console.log(this.payer.user_ethereum_id)
      console.log(this.id)
      const config = {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      }
      axios.post('http://localhost:5000/onboard', qs.stringify(this.payer), config).then(response => {
        console.log(response)
      })
    }
  },
  props: {
    name: String,
    service: String,
    id: Number
  }
}
</script>

<style lang="scss" scoped>
.modal-backdrop {
  position: fixed;
  background-color: rgba(0, 0, 0, 0.3);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  // background-color: rgba(208, 191, 175, 1) !important;
  background-color: rgba(0, 0, 0, 1) !important;
  border-radius: 4px;
  box-shadow: 2px 2px 20px 1px;
  overflow-x: auto;
  display: flex;
  flex-direction: column;
  max-width: 50%;
  max-height: 40%;
  top: 25%;
  left: 25%;
}

.modal-header,
.modal-footer {
  padding: 15px;
  display: flex;
}

.modal-header {
  color: #ffc312;;
  justify-content: space-between;
}

.modal-footer {
  justify-content: flex-end;
  padding: 1.2em 2em;
}

.modal-body {
  position: relative;
  padding: 2em;
}

.btn-close {
  border: none;
  font-size: 14px;
  padding: 6px 8px;
  cursor: pointer;
  font-weight: bold;
  color: black;
  background: transparent;
  background-color: #ffc312;

  i {
    display: block;
  }
}

.btn-primary {
  color: black;
  background-color: #ffc312;
  border-color: #ffc312;
  width: 100px;
}

.container {
  height: 100%;
  align-content: center;
}

.card {
  height: 370px;
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
