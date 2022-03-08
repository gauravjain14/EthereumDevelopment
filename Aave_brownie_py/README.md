Note: no contracts are deployed in this since all the contracts are already on-chain

## Objective:

1. Swap our Eth to Weth*
2. Deposit some Eth into Aave
3. Borrow some assert with the Eth collateral
    - Sell that borrowed asset. (Short selling)
4. Repay everything back.

* Aave converts the deposited Eth to Weth, since the contract deployed uses a Weth Gateway.


## Contract addresses
1. Get the address of the Weth contract on Kovan Testnet
2. Address of Lending Pool can change, unlike a majority of the contracts
    - To get around this, there's an address provider that tells where Aave contracts are


## Testing:

1. Integration Testing: Kovan
2. Local Tests: Because we won't be deployed anything locally, we don't need to have 
    to deploy mocks and also we don't need oracle responses. Thus, we can just
    **mock** the `mainnet-fork`.