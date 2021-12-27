pragma solidity ^0.5.6;

// implement the ERC20 standard;
contract DappToken {
    // Constructor
    // Set the total number of tokens
    // Read the total number of tokens
    uint256 public totalSupply;
     
    constructor() public {
        totalSupply = 100000;
    }
}