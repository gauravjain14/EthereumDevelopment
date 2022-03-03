import time
from .helpful_scripts import get_account, get_contract, fund_with_link
from brownie import Lottery, network, config

def deploy_lottery():
    account = get_account() #id="brownie-freecodecamp-account")
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )

    print("Deployed Lottery Contract!")
    return lottery

def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # Get Entrace fees
    value = lottery.getEntranceFees({"from": account})

    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1) # Wait for the last transaction
    print("The lottery is started!")

    # We first need to fund the contract to be able to request randomness
    #fund_with_link(lottery.address, amount=100000000000000000)
    #print("Lottery is funded!")

def enter_lottery():
    account = get_account(index=0)
    print(f'account 1 {account}')
    lottery = Lottery[-1]
    value = lottery.getEntranceFees() + 50000000 # in Wei
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)

    account = get_account(index=1)
    print(f'account 2 {account}')
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1) # Wait for the last transaction
    print("Entered the lottery successfully!")

def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    print(f'Lottery is funded')
    ending_tx = lottery.endLottery({"from": account})
    # Since chainlink will call fulfillRandomness, should we wait for 2 txs?
    # But because we don't have the chainlink node on our local network, i.e.
    # ganache, this would be only 1 transaction
    ending_tx.wait(1) # Wait for the last transaction
    time.sleep(120)
    print("The lottery is ended!")

def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()