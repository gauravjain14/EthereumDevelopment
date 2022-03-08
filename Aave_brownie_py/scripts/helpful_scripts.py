from brownie import (
    network, 
    accounts, 
    config,
    Contract,
    interface
)
import web3
from web3 import Web3

DECIMALS = 18
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

def get_account(index=None, id=None):
    if id:
        return accounts.load(id)
    if (network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or
        network.show_active() in FORKED_LOCAL_ENVIRONMENTS):
        if index:
            return accounts[index]
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])


def get_contract():
    """
    We won't deploy any mocks and use mainnet-fork for testing
    """
    return interface.IWeth(config["networks"][network.show_active()]["weth_token"])