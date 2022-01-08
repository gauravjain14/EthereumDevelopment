pragma solidity ^0.5.6;

import "./DappToken.sol";
// See how to import library
// import "https://github.com/dapphub/ds-math/blob/master/src/math.sol";

contract DappTokenSale {
    address payable admin; // state variabe
    DappToken public tokenContract;
    uint256 public tokenPrice;
    uint256 public tokensSold;

    event Sell(address _buyer, uint256 _amount);

    constructor(DappToken _tokenContract, uint256 _tokenPrice) public {
        // Assign an admin. External account on the blockchain
        admin = msg.sender;
        // Token Contract
        tokenContract = _tokenContract;
        // Token Price
        tokenPrice = _tokenPrice;
    }
    
    function multiply(uint x, uint y) internal pure returns (uint z) {
        require(y == 0 || (z = x * y) / y == x);
    }


    // payable is modifier that allows a function in solidity to receive ether
    function buyTokens(uint256 _numberOfTokens) public payable {
        // require that the value is equal to tokens * tokenPrice
        require(msg.value == multiply(_numberOfTokens, tokenPrice));

        // require that there are enough tokens in the contract
        require(tokenContract.balanceOf(address(this)) >= _numberOfTokens);

        // require that a transfer is successful
        // this can be carried out by transferring tokens using transfer
        require(tokenContract.transfer(msg.sender, _numberOfTokens));

        // keep track of the tokens sold
        tokensSold += _numberOfTokens;

        // trigger a Sell Event
        // buyer - msg.sender
        emit Sell(msg.sender, _numberOfTokens);
    }

    function endSale() public {
        // only the admin can do this.
        require(msg.sender == admin);

        // Transfer the remaining Dapp tokens to the admin
        // This require transfers the funds.
        require(tokenContract.transfer(admin, tokenContract.balanceOf(address(this))));

        // looks like selfdestruct is no longer advised.
        // Then why do we need to transfer funds to the admin again?
        admin.transfer(address(this).balance);
    }
}