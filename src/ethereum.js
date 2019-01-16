import Web3 from 'web3'
import { PromiseObservable } from 'rxjs/observable/PromiseObservable'

const getWeb3 = () => {
  return new Promise(async (resolve, reject) => {
    // const web3Provider = new Web3.providers.HttpProvider('http://localhost:7545')
    // var web3Provider
    // if (window.ethereum) {
    //     web3Provider = window.ethereum
    //     try {
    //         await window.ethereum.enable()
    //         console.log("Got web3Provider from window ethereum")
    //     } catch (error) {
    //         reject('User denied account access')
    //     }
    // }
    // else if (window.web3) {
    //     web3Provider = window.web3.currentProvider
    //     console.log("Got web3Provider from window web3")
    // }
    // else {
    //     web3Provider = new Web3.providers.HttpProvider('http://localhost:7545')
    //     console.log("new web3Provider")
    // }
    var web3Provider = window.ethereum
    try {
      await window.ethereum.enable()
      console.log('Got web3Provider from window ethereum')
    } catch (error) {
      reject('User denied account access')
    }
    const web3 = window.web3
    resolve(web3)
  })
}

const getContract = (web3Client, contractABI, contractAddr) => {
  return new Promise((resolve, reject) => {
    console.log(web3Client)
    var paymentContract = web3Client.eth.contract(contractABI)
    resolve(paymentContract.at(contractAddr))
  })
}

const payContract = (paymentContract, amountDue) => {
  return new Promise((resolve, reject) => {
    web3.eth.getAccounts((error, accounts) => {
      if (error) {
        console.log(error)
        reject(error)
      }
      console.log(paymentContract)
      paymentContract.pay({
        from: accounts[0],
        value: amountDue
      })
      resolve(res)
    })
  })
}
export default {
  getWeb3,
  getContract,
  payContract
}
