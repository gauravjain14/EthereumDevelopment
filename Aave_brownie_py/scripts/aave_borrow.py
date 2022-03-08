from brownie import config, network, interface
from .helpful_scripts import get_account
from .get_weth import get_weth
from web3 import Web3

TESNET_ENVIRONMENTS = ["kovan"]

# amount - Fixed for now
amount = Web3.toWei(0.1, "ether")

def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    
    # if on mainnet-fork
    if network.show_active() in ["mainnet-fork"]:
        get_weth(account=account)
    # ABI
    # address of the lending pool contract
    lending_pool = get_lending_pool()
    print(f'Lending Pool contract address @ {lending_pool}')

    # Approve the lending pool to spend our ETH
    approve_erc20(amount, lending_pool.address, erc20_address, account)

    # Now deposit the amount
    print("Depositing...")
    tx = lending_pool.deposit(erc20_address, amount, account, 0, {"from": account})
    tx.wait(1)
    print("Deposit successfully completed")

    # Now we can borrow another asset
    # Let's check borrowable stats
    borrowable_eth, total_debt = get_borrowable_data(lending_pool, account)

    # DAI in terms of Eth
    # We need this because we need to know how much DAI can we borrow.
    dai_eth_price = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
    )

    # 0.95 is a buffer factor to maintain our health status
    amount_dai_to_borrow = (1 / dai_eth_price) * borrowable_eth * 0.95
    print(f'We can borrow {amount_dai_to_borrow} DAI')

    if network.show_active() in TESNET_ENVIRONMENTS:
        dai_token_address = get_dai_token_address('DAI')
        if not dai_token_address:
            return "Failed To get DAI Token Address on Testnet"
    else:
        dai_token_address = config["networks"][network.show_active()]["dai_token"]
    
    borrow_tx = lending_pool.borrow(
        dai_token_address,
        amount_dai_to_borrow,
        1,
        0,
        account,
        {"from": account}
    )
    borrow_tx.wait(1)


def approve_erc20(amount, spender, erc20_address, account):
    # ABI
    # approve
    print(f'Approving the ERC20 token...')
    erc20 = interface.ERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("Approved!")
    pass


def get_lending_pool():
    lending_pool_address_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_address_provider"]
    )
    lending_pool_address = lending_pool_address_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool


def get_borrowable_data(lending_pool, account):
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        loan_to_value,
        health_factor
    ) = lending_pool.getUserAccountData(account.address)
    
    # All eth returned is in Wei. Convert to ether
    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")

    print(f'You have {total_collateral_eth} worth of Eth deposited.')
    print(f'You have {total_debt_eth} worth of Eth in debt.')
    print(f'You have {available_borrow_eth} worth of Eth available to borrow.')
    return (float(available_borrow_eth), float(total_debt_eth))


def get_asset_price(price_feed_address):
    # ABI
    # Address
    dai_eth_price_feed = interface.AggregatorV3Interface(price_feed_address)
    (_, price, _, _, _) = dai_eth_price_feed.latestRoundData()
    latest_price_ether = Web3.fromWei(price, "ether")
    print(f'The DAI/ETH price is {price}')
    return float(latest_price_ether)


def get_dai_token_address(token_to_query):
    lending_pool_address_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_address_provider"]
    )
    protocol_data_provider = interface.IProtocolDataProvider(
        config["networks"][network.show_active()]["protocol_data_provider"]
    )
    all_tokens = protocol_data_provider.getAllReservesTokens()
    all_tokens = [{k: v for k,v in zip(keys, tup)} for tup in all_tokens]
    return all_tokens[token_to_query]


