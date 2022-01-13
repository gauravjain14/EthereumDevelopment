const { sendAndConfirmTransaction } = require("@solana/web3.js");

var DappToken = artifacts.require("./DappToken.sol");
var DappTokenSale = artifacts.require("./DappTokenSale.sol");

contract("DappTokenSale", function(accounts) {
    var tokenInstance;
    var tokenSaleInstance;
    var admin = accounts[0];
    var buyer = accounts[1];
    var tokensAvailable = 75000;
    var numberOfTokens;
    var tokenPrice = web3.utils.toWei("0.01", "ether");; // in wei

    it('initialize the contract with the correct values', function() {
        return DappTokenSale.deployed().then(function(instance){
            tokenSaleInstance = instance;
            return tokenSaleInstance.address;
        }).then(function(address) {
            assert.notEqual(address, 0x0, 'has contract address');
            return tokenSaleInstance.tokenContract();
        }).then(function(address) {
            assert.notEqual(address, 0x0, 'has token contract address');
            return tokenSaleInstance.tokenPrice();
        }).then(function(price) {
            assert.equal(price, tokenPrice, 'token price is correct');
        });
    });

    it('facilitates token buying', function() {
        return DappToken.deployed().then(function(instance){
            tokenInstance = instance;
            return DappTokenSale.deployed();
        }).then(function(instance){
            tokenSaleInstance = instance;
            // provision 75% of the tokens that exist.
            return tokenInstance.transfer(tokenSaleInstance.address, tokensAvailable, {from: admin});
        }).then(function(receipt) {
            return tokenInstance.balanceOf(tokenSaleInstance.address);
        }).then(function(contractBalance) {
            console.log('smart contract has the balance of ', contractBalance.toNumber());
            return tokenInstance.balanceOf(admin);
        }).then(function(adminBalance) {
            console.log(adminBalance.toNumber());
            numberOfTokens = 10;
            return tokenSaleInstance.buyTokens(numberOfTokens, {from: buyer,
                value: numberOfTokens * tokenPrice})
        }).then(function(receipt) {
            assert.equal(receipt.logs.length, 1, 'triggers one event');
            assert.equal(receipt.logs[0].event, 'Sell', 'should be "Sell" event');
            assert.equal(receipt.logs[0].args._buyer, buyer, 'logs the account that purchased the tokens');
            assert.equal(receipt.logs[0].args._amount, numberOfTokens, 'logs the number of tokens purchased');
            return tokenSaleInstance.tokensSold();
        }).then(function(amount) {
            assert.equal(amount.toNumber(), numberOfTokens, 'increments the number of tokens sold');
            return tokenInstance.balanceOf(tokenSaleInstance.address);
        }).then(function(amount) {
            console.log('token sale balance ', amount.toNumber());
        })
    });

    it('ends token sale', function() {
        return DappToken.deployed().then(function(instance) {
            tokenInstance = instance;
            return DappTokenSale.deployed();
        }).then(function(instance) {
            tokenSaleInstance = instance;
            // try to end the token sale by anyone but the admin.
            return tokenSaleInstance.endSale({from: admin});
        }).then(function(receipt) {
            return tokenInstance.balanceOf(admin);
        }).then(function(balance) {
            console.log(balance.toNumber());
        });
        /*}).then(function(receipt) {
            return tokenInstance.balanceOf(admin);
        }).then(function(balance) {
            console.log(balance.toNumber());
            assert.equal(balance.toNumber(), 99990, 'return all dapps not sold by the admin');
        });*/
    });
});