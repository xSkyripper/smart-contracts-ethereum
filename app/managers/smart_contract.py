from web3 import Web3
from solc import compile_files
from app.models import Contract as ContractModel, User as UserModel

# Constants
PAYMENT_STATUS_OK = 0


class SmartContractManager(object):
    def __init__(self, eth_network_addr, default_account=None):
        self._web3 = Web3(Web3.HTTPProvider(eth_network_addr))
        self._web3.eth.defaultAccount = default_account or w3.eth.accounts[0]
        self.eth_contract = None

    def create_contract(self, contract_file_path, contract_name):
        compiled_sol = compile_files([contract_file_path])
        contract_interface = compiled_sol([f'{contract_file_path}:{contract_name}'])

        contract_object = self._web3.eth.contract(abi=contract_interface['abi'],
        bytecode=contract_interface['bin'])

        tx_hash = contract_object.constructor().transact()
        tx_receipt = self._web3.eth.waitForTransactionReceipt(tx_hash)

        return tx_receipt.contractAddress, contract_interface['abi']

    def set_contract(self, contract_eth_addr, contract_abi):
        self.eth_contract = self._web3.eth.contract(address=contract_eth_addr, abi=contract_abi)
        
    def add_user_to_contract(self, user_eth_addr):
        self.eth_contract.functions.add_user(user_eth_addr)

    def check_payment_status(self):
        payment_status = self.etc_contract.functions.get_payment_status().call()
        return payment_status == PAYMENT_STATUS_OK

    def retrieve_ethereum_from_contract():
        print("Calling 'retrieve_ethereum' method: {}"
              .format(self.eth_contract.functions.retrieve_ethereum().call()))

