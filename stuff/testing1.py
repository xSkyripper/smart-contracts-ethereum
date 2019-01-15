from app.ethereum import Manager as SCManager, PaymentContract
import IPython
import logging
import os
import os.path
from app import create_app, web3

logging.getLogger('smart_contract').setLevel(level=logging.INFO)

app = create_app(os.getenv('FLASK_CONFIG', 'development'))

contract_owner = app.config['ETH_CONTRACT_OWNER']
contract_file_path = os.path.join(app.config['ETH_CONTRACTS_DIR'],
                                  app.config['ETH_CONTRACTS']['payment']['filename'])
contract_name = app.config['ETH_CONTRACTS']['payment']['name']
contract_amount_due = 1000000000000000000 # 1 ether
scm = SCManager(web3)
# contract_eth_addr = scm.create_contract(contract_owner,
#                                         contract_file_path,
#                                         contract_name,
#                                         contract_amount_due)
contract_build_path = SCManager.get_contract_build_path(contract_file_path)
contract_abi, _ = SCManager.load_contract_build(contract_build_path)

contract_eth_addr = '0x79337b477DCd8F6b2e10056e925b4Ea72FEf8865'
pc = PaymentContract(web3_client=web3,
                     owner=contract_owner,
                     contract_eth_addr=contract_eth_addr,
                     contract_abi=contract_abi)

# r = pc.remove_payer('0x2d337E1AB8AD8a5DBFfD6aC06f8E55F2E09bDf23')
# r = pc.add_payer('0x2d337E1AB8AD8a5DBFfD6aC06f8E55F2E09bDf23')
# r = pc.add_payer('0x32ae6e2418e99CdeFAE8173EA6B631F4891deCb4')
payers = pc.get_payers()
# amount_due = pc.get_amount_due()
# contract_balance = pc.get_contract_balance()

IPython.embed()


