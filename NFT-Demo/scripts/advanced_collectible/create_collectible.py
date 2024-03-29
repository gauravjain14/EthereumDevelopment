from brownie import AdvancedCollectible
from scripts.helpful_scripts import fund_with_link, get_account
from web3 import Web3

def main():
    account = get_account()
    advanced_collectible = AdvancedCollectible[-1]
    print("Advanced Collectible contract at {0}".format(advanced_collectible.address))
    fund_with_link(advanced_collectible.address, amount=Web3.toWei(0.1, "ether"))
    creation_tx = advanced_collectible.createCollectible({"from": account})
    creation_tx.wait(1)
    print("Collectible created!")