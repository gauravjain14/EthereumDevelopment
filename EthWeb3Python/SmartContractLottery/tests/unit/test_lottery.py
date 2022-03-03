from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
    fund_with_link
)
import brownie
from brownie import Lottery, accounts, config, network, exceptions
from scripts.deploy_lottery import deploy_lottery
from web3 import Web3
import pytest

# 0.019
# 190000000000000000

from brownie import Lottery, accounts, config, network
from web3 import Web3

def test_get_entrance_fee():
    account = accounts[0]
    lottery = deploy_lottery()
    # expected_entrance_fee = Web3.toWei()
    entrance_fee = lottery.getEntranceFees()
    print(f'Entrance Fee {entrance_fee}')
    # toWei conversion is dependent on the eth to usd price
    assert lottery.getEntranceFees() > Web3.toWei(0.0001, "ether")
    # assert lottery.getEntranceFees() < Web3.toWei(0.022, "ether")


def test_cant_enter_without_min_fees():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    lottery.startLottery()

    # Pytest raises an exception if lottery cannot be entered.
    # If instead, the exception is not raised, the check will fail and
    # execution is aborted
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({
            "from": get_account(),
            "value": lottery.getEntranceFees() - 1000000
        })


def test_can_start_and_enter_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account() # this is the owner as well
    lottery.startLottery({"from": account})
    # Enter Lottery with min entranceFees
    lottery.enter({"from": get_account(index=1), "value": lottery.getEntranceFees()})
    assert lottery.players(0) == get_account(index=1)


def test_end_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFees()})
    fund_with_link(lottery, account, get_contract("link_token"))
    transaction = lottery.endLottery({"from": account})
    time.sleep(120) # Is there a better way than setting a timeout clock?


def test_can_end_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFees()})
    lottery.enter({"from": get_account(index=1), "value": lottery.getEntranceFees()})
    lottery.enter({"from": get_account(index=2), "value": lottery.getEntranceFees()})
    fund_with_link(lottery, account, get_contract("link_token"))
    print(lottery.balance())
    print(account.balance())

    # End lottery transaction
    transaction = lottery.endLottery({"from": account})
    request_id = transaction.events["RequestedRandomness"]["requestId"]
    SEED = 777
    balance_of_lottery = lottery.balance()
    starting_balance_of_lottery = account.balance()
    get_contract("vrf_coordinator").callBackWithRandomness(
                                                        request_id,
                                                        SEED,
                                                        lottery.address,
                                                        {"from": account})
    # Lottery Winner = recent_winner % 3
    assert lottery.recentWinner() == account # 0th account
    assert lottery.balance() == 0 # amount transferred to account
    assert account.balance() == starting_balance_of_lottery + balance_of_lottery