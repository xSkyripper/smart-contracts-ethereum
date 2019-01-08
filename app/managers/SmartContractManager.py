from web3 import Web3
from app.models import Contract as ContractModel, User as UserModel

# Constants
PAYMENT_STATUS_OK = 0


def add_user_to_contract(user, contract_id):
    contract = get_contract(contract_id)
    contract.functions.add_user(user)
    return 0

def check_payment_status(contract_id):
    contract = get_contract(contract_id)
    payment_status = contract.functions.get_payment_status().call()
    return (payment_status == PAYMENT_STATUS_OK)

def retrieve_ethereum_from_contract(contract_id):
    contract = get_contract(contract_id)
    print("Calling 'retrieve_ethereum' method: {}".format(
        contract.functions.retrieve_ethereum().call()
    ))

def get_contract(contract_id)
{
    db_contract = ContractModel.query.get(contract_id)

    if not db_contract:
        return null
    
    eth_contract = w3.eth.contract(address=db_contract.ethereum_addr,
                              abi=db_contract.abi,)

    return eth_contract
}