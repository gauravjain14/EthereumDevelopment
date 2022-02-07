from brownie import FundMe
from .helpful_scripts import get_account

def fund():
    fund_me = FundMe[-1]
    entrance_fee = fund_me.getEntranceFee()
    print("entry fee ", entrance_fee)

def main():
    fund()