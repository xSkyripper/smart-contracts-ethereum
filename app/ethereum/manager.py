import logging
import json
import os.path
from hexbytes import HexBytes
from flask_web3 import current_web3
from easysolc import Solc

logger = logging.getLogger(__name__)


class Manager(object):
    def __init__(self, web3_client=None):
        self._web3 = web3_client or current_web3

    @classmethod
    def get_contract_build_path(cls, contract_path):
        contract_dirname = os.path.dirname(contract_path)
        contract_filename = os.path.basename(contract_path)
        contract_abi_filename = os.path.splitext(contract_filename)[0] + '_build.json'

        return os.path.join(contract_dirname, contract_abi_filename)
    
    @classmethod
    def save_contract_build(cls, contract_abi, contract_bin, contract_build_path):
        contract_build = dict(contract_abi=contract_abi, contract_bin=contract_bin.hex())

        with open(contract_build_path, 'w+') as fd:
            json.dump(contract_build, fd, indent=4)

        logger.info('Saved contract build to path "%s"', contract_build_path)

    @classmethod
    def load_contract_build(cls, contract_build_path):
        with open(contract_build_path, 'r') as fd:
            data = json.load(fd)
        
        return data['contract_abi'], HexBytes(data['contract_bin'])

    @classmethod
    def compile_contract(cls, contract_path, contract_name, solc_path='', save=True):
        solc = Solc(solc_path)

        logger.info('Compiling contract from path "%s", named "%s" ...',
                    contract_path, contract_name)
        compiled_contract = solc.get_contract_instance(source=contract_path, 
                                                       contract_name=contract_name)
        logger.info('Compiled contract!')

        if save:
            contract_build_path = cls.get_contract_build_path(contract_path)
            cls.save_contract_build(compiled_contract.abi, compiled_contract.bytecode, contract_build_path)

        return compiled_contract

    def push_contract_to_ethereum(self, owner, contract_abi, contract_bin, *contract_args):
        contract = self._web3.eth.contract(abi=contract_abi, bytecode=contract_bin)

        logger.info('Pushing contract to Ethereum ...')
        tx_hash = contract.constructor(*contract_args).transact({'from': owner})
        tx_receipt = self._web3.eth.waitForTransactionReceipt(tx_hash)
        logger.info('Pushed contract for owner "{}" with args "{}"'.format(owner, *contract_args))

        logger.info('Ethereum address of the contract is "%s"', tx_receipt.contractAddress)
        return tx_receipt.contractAddress

    def create_contract(self, owner, contract_path, contract_name, *contract_args, compile=False):
        contract_build_path = self.get_contract_build_path(contract_path)

        if compile or not os.path.exists(contract_build_path):
            logger.info('Contract build for "%s" does not exist')
            compiled_contract = self.compile_contract(contract_path, contract_name)
            contract_abi, contract_bin = compiled_contract.abi, compiled_contract.bytecode
        else:
            contract_abi, contract_bin = self.load_contract_build(contract_build_path)

        contract_addr = self.push_contract_to_ethereum(owner, contract_abi, contract_bin, *contract_args)

        return contract_addr

