from brownie import (
    network, 
    accounts, 
    config,
    VRFCoordinatorMock,
    LinkToken,
    Contract,
    interface
)
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
# url/contract_address/token_id
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"

def get_account(index=None, id=None):
    if id:
        return accounts.load(id)
    if (network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or
        network.show_active() in FORKED_LOCAL_ENVIRONMENTS):
        if index:
            return accounts[index]
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])

contract_to_mock = {"vrf_coordinator": VRFCoordinatorMock,
                    "link_token": LinkToken}


def get_contract(contract_name):
    """
    This function will grab the contract addresses from the brownie config if
    defined otherwise, it will deploy a mock contract
        Args: contract_name
        Returns:
            brownie.network.contract.ProjectContract: Most recently deployed
                version of the account
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # this is equivalent to MockV3Aggregator.length
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(contract_type._name, contract_address,
                                    contract_type.abi)

    return contract


DECIMALS = 8
INITIAL_VALUE = 20000000000000
def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    print(f"The active network is {network.show_active()}")
    print("Deploying the mock smart contract...")
    # check if the contract is already deployed
    # once the contract is deployed, it is added to the list
    account = get_account()
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(
        link_token.address, {"from": account}
    )
    print("Contracts Deployed!")


def fund_with_link(contract_address, # Lottery contract address
                account=None,
                link_token=None,
                amount=100000000000000000): # 0.1 LINK
    account = account if account else get_account() # index=0 default owner
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})    
    # LinkTokenInterface requires the link_token contract address
    # returns the Link Token Contract
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # tx = link_token_contract.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Funding the contract {link_token.address} completed!")
    return tx