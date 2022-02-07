from brownie import accounts, config, network, FundMe, MockV3Aggregator
from .helpful_scripts import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from web3 import Web3

def deploy_fund_me():
    account = get_account()
    # if we are on a persistent network, like rinkeby test network, we use
    # the associated contract otherwise, call a mock contract in contracts/test
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
        print(price_feed_address)

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        # publish_source=True, # this can't be done on the mock network
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"contract deployed at {fund_me.address}")

def main():
    print(network.show_active())
    deploy_fund_me()