## Integration testing on the Rinkeby Test chain

from brownie import network
import pytest
from scripts.helpful_scripts import (
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    fund_with_link
)
from scripts.deploy_lottery import deploy_lottery
import time

def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    print(account)
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFees()})
    lottery.enter({"from": account, "value": lottery.getEntranceFees()})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})
    time.sleep(120)
    assert lottery.recentWinner() == account
    assert lottery.balance == 0