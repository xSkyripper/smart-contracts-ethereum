from web3 import Web3
from easysolc import Solc
from app.models import Contract as ContractModel, User as UserModel
import logging
import json
import os.path

logger = logging.getLogger(__name__)

class SmartContractManager(object):
    def __init__(self,
                 eth_network_addr,
                 owner,
                 solc_path='',
                 ):
        self._solc = Solc(solc_path)
        self._web3 = Web3(Web3.HTTPProvider(eth_network_addr))
        self._web3.eth.defaultAccount = owner

    @staticmethod
    def _build_abi_path(contract_path):
        contract_dirname = os.path.dirname(contract_path)
        contract_filename = os.path.basename(contract_path)
        contract_abi_filename = os.path.splitext(contract_filename)[0] + '_abi.json'

        return os.path.join(contract_dirname, contract_abi_filename)

    @staticmethod
    def _save_contract_abi(contract_abi, contract_abi_path):
        with open(contract_abi_path, 'w+') as fd:
            json.dump(contract_abi, fd, indent=4)

    @staticmethod
    def get_contract_abi(contract_abi_path):
        contract_abi = None
        with open(contract_abi_path, 'r') as fd:
            contract_abi = json.load(fd)
        return contract_abi

    def _compile_contract(self, contract_file_path, contract_name):
        logger.info('Creating contract from path "%s", named "%s"', contract_file_path, contract_name)
        compiled_contract = self._solc.get_contract_instance(source=contract_file_path,
                                                             contract_name=contract_name)
        
        return compiled_contract

    def _push_contract_to_ethereum(self, compiled_contract, amount_due):
        contract_object = self._web3.eth.contract(abi=compiled_contract.abi,
                                                  bytecode=compiled_contract.bytecode)

        tx_hash = contract_object.constructor(amount_due).transact()
        tx_receipt = self._web3.eth.waitForTransactionReceipt(tx_hash)

        logger.info('Contract with amount due "%d" with address "%s" pushed to Ethereum',
                    amount_due, tx_receipt.contractAddress)
        return tx_receipt.contractAddress, compiled_contract.abi


    def create_contract(self, contract_path, contract_name, amount_due, persist=True):
        compiled_contract = self._compile_contract(contract_path, contract_name)
        logger.info('Created contract. Pushing to Ethereum network ...')
        contract_addr, contract_abi = self._push_contract_to_ethereum(compiled_contract, amount_due)

        if persist:
            contract_abi_path = self._build_abi_path(contract_path)
            logger.info("Writing ABI to path %s", contract_abi_path)
            self._save_contract_abi(contract_abi, contract_abi_path)

        return contract_addr, contract_abi


class PaymentContract(object):
    def __init__(self, eth_network_addr, contract_eth_addr, contract_path, owner=None):
        self._web3 = Web3(Web3.HTTPProvider(eth_network_addr))
        self._owner = owner
        self._contract_eth_addr = contract_eth_addr
        self._contract_path = contract_path
        self._contract_abi = SmartContractManager.get_contract_abi(
            SmartContractManager._build_abi_path(contract_path))
        self._contract = self._web3.eth.contract(address=contract_eth_addr, abi=self._contract_abi)

    def close(self):
        tx_hash = self._contract.functions.close().transact({'from': self._owner})
        return self._web3.eth.waitForTransactionReceipt(tx_hash)

    def add_payer(self, user_eth_addr):
        tx_hash = self._contract.functions.addPayer(user_eth_addr).transact({'from': self._owner})
        return self._web3.eth.waitForTransactionReceipt(tx_hash)

    def get_payers(self):
        return self._contract.functions.getPayers().call()

    def remove_payer(self, user_eth_addr):
        tx_hash = self._contract.functions.removePayer(user_eth_addr).transact({'from': self._owner})
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

