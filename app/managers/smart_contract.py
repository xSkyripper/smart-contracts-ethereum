import logging
import json
import os.path
from web3 import Web3
from easysolc import Solc

logger = logging.getLogger(__name__)


class Manager(object):
    def __init__(self, web3_client):
        self._web3 = web3_client

    @classmethod
    def build_abi_path(cls, contract_path):
        contract_dirname = os.path.dirname(contract_path)
        contract_filename = os.path.basename(contract_path)
        contract_abi_filename = os.path.splitext(contract_filename)[0] + '_abi.json'

        return os.path.join(contract_dirname, contract_abi_filename)

    @classmethod
    def persist_contract_abi(cls, contract_abi, contract_abi_path):
        with open(contract_abi_path, 'w+') as fd:
            json.dump(contract_abi, fd, indent=4)
    
    @classmethod
    def save_contract_abi(cls, contract_abi, contract_path):
        contract_abi_path = cls.build_abi_path(contract_path)
        cls.persist_contract_abi(contract_abi, contract_abi_path)
        logger.info('Written contract ABI to path "%s"', contract_abi_path)

    @classmethod
    def get_contract_abi(cls, contract_abi_path):
        with open(contract_abi_path, 'r') as fd:
            return json.load(fd)

    @classmethod
    def compile_contract(cls, contract_file_path, contract_name, solc_path=''):
        logger.info('Creating contract from path "%s", named "%s"',
                    contract_file_path, contract_name)
        solc = Solc(solc_path)
        compiled_contract = solc.get_contract_instance(source=contract_file_path,
                                                       contract_name=contract_name)

        return compiled_contract

    def push_contract_to_ethereum(self, compiled_contract, *contract_args):
        contract_object = self._web3.eth.contract(abi=compiled_contract.abi,
                                                  bytecode=compiled_contract.bytecode)


        tx_hash = contract_object.constructor(*contract_args).transact()
        tx_receipt = self._web3.eth.waitForTransactionReceipt(tx_hash)

        logger.info('Pushed contract with args "{}"'.format(*contract_args))
        logger.info('Ethereum address of the contract is "%s"', tx_receipt.contractAddress)
        return tx_receipt.contractAddress, compiled_contract.abi


    def create_contract(self, contract_path, contract_name, *contract_args, save=True):
        compiled_contract = self.compile_contract(contract_path, contract_name)
        logger.info('Created contract. Pushing to Ethereum network ...')
        contract_addr, contract_abi = self.push_contract_to_ethereum(compiled_contract, *contract_args)
        if save:
            self.save_contract_abi(contract_abi, contract_path)

        return contract_addr


class PaymentContract(object):
    def __init__(self,
                 web3_client,
                 contract_eth_addr,
                 contract_abi,
                 owner=None):
        self._web3 = web3_client
        self.owner = owner or web3_client.eth.defaultAccount
        self._contract = web3_client.eth.contract(address=contract_eth_addr, abi=contract_abi)

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

