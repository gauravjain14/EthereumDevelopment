from .helpful_scripts import get_account, get_contract
from brownie import accounts, interface, config, network

def main():
    get_weth()


def get_weth(account=None):
    """
    Mints Weth by depositing Eth
    """
    ### ABI and Address of the Weth contract
    ### Using Weth interface.
    account = (
        account if account else accounts.add(config["wallets"]["from_key"])
    )
    weth = get_contract()
    # deposit some amount to the contract
    tx = weth.deposit({"from": account, "value": 0.1*10**18})
    tx.wait(1)
    print(f'Received 0.1 Weth')