from web3 import Web3
from solc import compile_files


ETHEREUM_NET = "http://127.0.0.1:8545"
w3 = Web3(Web3.HTTPProvider(ETHEREUM_NET))
w3.eth.defaultAccount = w3.eth.accounts[0]


def main():
    print("=== Experiment 1: Hello world on Private Ethereum Network ===")

    # Compile the Solidity
    print("Compiling 'hello_world.sol' ...")
    compiled_sol = compile_files(['hello_world.sol'])
    contract_interface = compiled_sol['hello_world.sol:Greeter']

    # Get contract object
    greeter_contract = w3.eth.contract(abi=contract_interface['abi'],
                                       bytecode=contract_interface['bin'])

    # Deploy the contract and get the address
    print("Deploying contract to network ...")
    tx_hash = greeter_contract.constructor().transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    print("Deployed contract: {}".format(
        tx_receipt.contractAddress
    ))

    # Get contract instance
    greeter = w3.eth.contract(address=tx_receipt.contractAddress,
                              abi=contract_interface['abi'],)

    # Calling 'greet' method
    print("Calling 'greet' method: {}".format(
        greeter.functions.greet().call()
    ))

    # Setting greeting message
    print("Setting 'greet' message to 'Hello to Ethereum world' and waiting for transaction to be mined ...")
    tx_hash = greeter.functions.setGreeting('Hello to Ethereum world').transact()
    w3.eth.waitForTransactionReceipt(tx_hash)

    print("Updated contract greeting: {}".format(
        greeter.functions.greet().call()
    ))

    








if __name__ == "__main__":
    main()