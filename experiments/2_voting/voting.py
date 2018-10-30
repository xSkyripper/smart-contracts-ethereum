from web3 import Web3
from solc import compile_files
import sys

def main(ethereum_net_addr):
    w3 = Web3(Web3.HTTPProvider(ethereum_net_addr))
    w3.eth.defaultAccount = w3.eth.accounts[0]

    print("=== Experiment 2: Voting on Private Ethereum Network ===")

    # Compile the Solidity
    print("Compiling 'voting.sol' ...")
    compiled_sol = compile_files(['voting.sol'])
    contract_interface = compiled_sol['voting.sol:Voting']

    # Get contract object
    voting_contract = w3.eth.contract(abi=contract_interface['abi'],
                                       bytecode=contract_interface['bin'])

    # Deploy the contract and get the address
    print("Deploying contract to network ...")
    tx_hash = voting_contract.constructor().transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    print("Deployed voting contract: {}".format(
        tx_receipt.contractAddress
    ))

    # Get contract instance
    voting = w3.eth.contract(address=tx_receipt.contractAddress,
                              abi=contract_interface['abi'],)

    print("Voting for 'John' ...")
    tx_hash = contract.functions.voteForCandidate('John').transact()
    w3.eth.waitForTransactionReceipt(tx_hash)

    print("Voting for 'John' ...")
    tx_hash = contract.functions.voteForCandidate('John').transact()
    w3.eth.waitForTransactionReceipt(tx_hash)

    print("Voting for 'Alex' ...")
    tx_hash = contract.functions.voteForCandidate('Alex').transact()
    w3.eth.waitForTransactionReceipt(tx_hash)

    print("Voting for 'John' ...")
    tx_hash = contract.functions.voteForCandidate('John').transact()
    w3.eth.waitForTransactionReceipt(tx_hash)

    print("Total votes for 'John': {}".format(
        contract.functions.totalVotesFor('John').call()
    ))

    print("Total votes for 'Alex': {}".format(
        contract.functions.totalVotesFor('Alex').call()
    ))


if __name__ == "__main__":
    main(sys.argv[1])