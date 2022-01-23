import os
import json
import solcx
from solcx import compile_standard
from web3 import Web3
from dotenv import load_dotenv

# load all the variables from .env
load_dotenv()

solcx.install_solc('0.8.11')

''' A few notes from the script:
1. nonce is used on an address basis. For instance, if the account address
has not initiate any transaction yet, nonce = 0;
It should then be incremented with every transaction - deploying the smart
contract, calling the contract functions, etc. everything counts towards the
nonce.

2. For building a transaction, there are certain pieces of information requried
by the web3 API calls
 '''

with open("./SimpleStorage.sol", "r") as f:
    simple_storage_file = f.read()

# Compile Our Solidity
compiled_sol = compile_standard( 
    {
        "language" : "Solidity",
        "sources" : {"SimpleStorage.sol" : {"content" : simple_storage_file}},
        "settings" : {
            "outputSelection" : {
                "*" : {
                    "*" : ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        }
    },
    solc_version="0.8.11"
)

with open("compile_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"] \
    ["evm"]["bytecode"]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# for connecting to the Alchemy Rinkeby network
w3 = Web3(Web3.HTTPProvider("https://eth-rinkeby.alchemyapi.io/v2/EcVoouNQLC_a3_JnAJaPr37160XD3wei"))
chain_id = 4 # for rinkeby from chainid.network
my_account_address = "0xdBdE7bCa8880Ba655caf5CA136Df0e72eb083dDE"
private_key = os.getenv("PRIVATE_KEY")

# This creates a contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latest transaction -- this tells the number of transaction for this address
nonce = w3.eth.getTransactionCount(my_account_address)

# Building and sending the transaction
# 1. Build the transaction
# 2. Sign the transaction
# 3. Send the transaction
print("Deploying contract")
transaction = SimpleStorage.constructor().buildTransaction({"chainId": chain_id, \
     "from": my_account_address, "nonce": nonce})
# increment nonce
nonce += 1
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
# send this signed transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# blocking for the transaction to complete
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Contract deployed")

# Working with the contract
# We need - contract address, contract ABI
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Two ways to interact with a transaction
# Call -> don't make a state change to the blockchain. Can execute require calls
# Transact -> Actually make the state change

# Example - no state change
# Don't make this call on the testnet.
# print(simple_storage.functions.retrieve().call()) # should return zero
# print(simple_storage.functions.store(15).call())
# print(simple_storage.functions.retrieve().call())

## Initial the value favourite_number
print("Updating contract")
store_transaction = simple_storage.functions.store(256).buildTransaction(
    {"chainId": chain_id, "from": my_account_address, "nonce": nonce}
)
nonce += 1
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
send_signed_txn = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_signed_txn)
print(tx_receipt)
print("Contract Updated")
# now check the value at favourite_number
# Why doesn't simple_storage.functions.retrieve().transact() work here
print(simple_storage.functions.retrieve().call())