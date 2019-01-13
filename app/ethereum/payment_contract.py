class PaymentContract(object):
    def __init__(self,
                 contract_eth_addr,
                 contract_abi,
                 owner,
                 web3_client=None):
        self._web3 = web3_client or current_web3
        self.owner = owner
        self._contract = self._web3.eth.contract(address=contract_eth_addr, abi=contract_abi)

    def close(self):
        tx_hash = self._contract.functions.close().transact({'from': self.owner})
        return self._web3.eth.waitForTransactionReceipt(tx_hash)

    def add_payer(self, user_eth_addr):
        tx_hash = self._contract.functions.addPayer(user_eth_addr).transact({'from': self.owner})
        return self._web3.eth.waitForTransactionReceipt(tx_hash)

    def get_payers(self):
        return self._contract.functions.getPayers().call()

    def remove_payer(self, user_eth_addr):
        tx_hash = self._contract.functions.removePayer(user_eth_addr).transact({'from': self.owner})
        return self._web3.eth.waitForTransactionReceipt(tx_hash)

    def pay(self, user_eth_addr, value):
        tx_hash = self._contract.functions.pay().transact({'from': user_eth_addr, 'value': value})
        return self._web3.eth.waitForTransactionReceipt(tx_hash)

    def check_payment_status(self, user_eth_addr):
        return self._contract.functions.checkPaymentStatus(user_eth_addr).call()

    def get_amount_due(self):
        return self._contract.functions.getAmountDue().call()

    def get_contract_balance(self):
        return self._contract.functions.getContractBalance().call()
