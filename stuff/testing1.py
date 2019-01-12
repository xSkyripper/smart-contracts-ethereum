from app.managers.smart_contract import SmartContractManager, PaymentContract
import IPython
import logging

l = logging.getLogger('smart_contract')
logging.basicConfig(level=logging.INFO)

ethereum_net_addr = 'http://127.0.0.1:7545'
ethereum_default_account = '0xA6115D445B2D3DD2EBF9e7daEC2A135b4F750d02'
contract_file_path = 'app/contracts_files/Payment.sol'
contract_name = 'Payment'
contract_amount_due = 1000000000000000000 # 1 ether

smc = SmartContractManager(ethereum_net_addr, owner=ethereum_default_account)

# contract_eth_addr, contract_abi = smc.create_contract(contract_file_path, contract_name, contract_amount_due)
contract_eth_addr = '0x332C66F0444D13FbEeB5602cb24bffac3c636A78'

pc = PaymentContract(eth_network_addr=ethereum_net_addr,
                     contract_eth_addr=contract_eth_addr,
                     contract_path=contract_file_path,
                     owner=ethereum_default_account)

# r = pc.add_payer('0x2d337E1AB8AD8a5DBFfD6aC06f8E55F2E09bDf23')
# r = pc.add_payer('0x32ae6e2418e99CdeFAE8173EA6B631F4891deCb4')
# payers = pc.get_payers()
# amount_due = pc.get_amount_due()
# contract_balance = pc.get_contract_balance()

IPython.embed()
