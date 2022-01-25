from brownie import accounts, config, network, SimpleStorage
import os

def deploy_simple_storage():
    ''' Three different ways to import accounts in brownie '''
    # account = accounts[0] # brownie ganache accounts
    ## This is the command line approach
    # account = accounts.load("freecodecamp-account")
    # print(account)
    # account = accounts.add(os.getenv("PRIVATE_KEY"))
    # The following is because we have one canonical space where we'll pull our
    # private keys from
    account = get_account()
    # this will return a contract
    simple_storage = SimpleStorage.deploy({"from": account})
    # Brownie figures out whether it is a call or a transaction
    stored_value = simple_storage.retrieve()
    transaction = simple_storage.store(512, {"from": account})
    # wait(1) - how many blocks we should wait for
    transaction.wait(1)
    print(simple_storage.retrieve())

def get_account():
    # if working on a development chain, use accounts[0]
    if(network.show_active() == "development"):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def main():
    deploy_simple_storage()