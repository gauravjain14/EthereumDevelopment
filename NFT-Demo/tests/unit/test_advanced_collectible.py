from brownie import network, AdvancedCollectible
import pytest
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_contract, get_account
from scripts.advanced_collectible.deploy_and_create import deploy_and_create


def test_can_create_advanced_collectible():
    # deploy the contract
    # create an NFT
    # get a random breed back
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for Local Testing")
    # Act
    advanced_collectible, created_tx = deploy_and_create()
    requestId = created_tx.events["requestedCollectible"]["requestId"]
    # This imitates calling the fulfillRandomness function
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, 777, advanced_collectible.address, {"from": get_account()}
    )
    
    # Assert
    assert advanced_collectible.tokenCounter() == 1
