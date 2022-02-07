from brownie import network, accounts, config, MockV3Aggregator
from web3 import Web3

DECIMALS = 18
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

def get_account():
    # if working on a development chain, use accounts[0]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying the mock smart contract...")
    # check if the contract is already deployed
    # once the contract is deployed, it is added to the list
    if len(MockV3Aggregator) <= 0:
        print("creating a new contract")
        MockV3Aggregator.deploy(
            18, Web3.toWei(2000, "ether"), {"from": get_account()}
        )
    