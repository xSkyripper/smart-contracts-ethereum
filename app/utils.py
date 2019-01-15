import os.path
from app.ethereum import Manager as SCManager, PaymentContract

def get_payment_contract_abi(cfg):
        contract_file_path = os.path.join(cfg['ETH_CONTRACTS_DIR'],
                                          cfg['ETH_CONTRACTS']['payment']['filename'])
        contract_build_path = SCManager.get_contract_build_path(contract_file_path)
        contract_abi, _ = SCManager.load_contract_build(contract_build_path)

        return contract_abi

def get_payment_contract(cfg, web3, contract_eth_addr):
        contract_abi = get_payment_contract_abi(cfg)
        payment_contract = PaymentContract(web3_client=web3,
                                           owner=cfg['ETH_CONTRACT_OWNER'],
                                           contract_eth_addr=contract_eth_addr,
                                           contract_abi=contract_abi)
        return payment_contract

