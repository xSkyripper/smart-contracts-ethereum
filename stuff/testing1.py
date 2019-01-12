from app.managers.smart_contract import Manager as SCManager, PaymentContract
import IPython
import logging
from web3 import Web3

logging.getLogger('smart_contract').setLevel(level=logging.INFO)

web3_client = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
web3_client.eth.defaultAccount = '0xA6115D445B2D3DD2EBF9e7daEC2A135b4F750d02'

contract_file_path = 'app/contracts_files/Payment.sol'
contract_name = 'Payment'
contract_amount_due = 1000000000000000000 # 1 ether
scm = SCManager(web3_client)
contract_eth_addr = scm.create_contract(contract_file_path, contract_name, contract_amount_due)

# contract_eth_addr = '0x1D52CE6C16748aA1DbC7B0Fad696a3e1dd8549e6'
# contract_abi_path = SCManager.build_abi_path(contract_file_path)
# contract_abi = SCManager.get_contract_abi(contract_abi_path)
# pc = PaymentContract(web3_client=web3_client,
#                      contract_eth_addr=contract_eth_addr,
#                      contract_abi=contract_abi)

# r = pc.add_payer('0x2d337E1AB8AD8a5DBFfD6aC06f8E55F2E09bDf23')
# r = pc.add_payer('0x32ae6e2418e99CdeFAE8173EA6B631F4891deCb4')
# payers = pc.get_payers()
# amount_due = pc.get_amount_due()
# contract_balance = pc.get_contract_balance()

# IPython.embed()
