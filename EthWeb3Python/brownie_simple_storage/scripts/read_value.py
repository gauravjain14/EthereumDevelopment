from brownie import SimpleStorage, accounts, config

def read_contract():
    # deployed contract is stored in build/deployments and can be easily
    # read as SimpleStorage[index]
    # SimpleStorage[-1] gets us the most recent deployment
    simple_storage = SimpleStorage[-1]
    print(simple_storage.retrieve())

def main():
    read_contract()