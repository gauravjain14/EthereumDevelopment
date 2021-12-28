var DappToken = artifacts.require("./DappToken.sol");

contract('DappToken', function(accounts) {
    // why do we need to define this is as a var if we can access it everywhere 
    var tokenInstance;

    it('initializes the contract with the correct values', function() {
        return DappToken.deployed().then(function(instance){
            tokenInstance = instance;
            return tokenInstance.name();
        }).then(function(name) {
            assert.equal(name, 'DApp Token', 'has the correct name');
            return tokenInstance.symbol();
        }).then(function(symbol) {
            assert.equal(symbol, 'DApp', 'Symbol matches');
        });
    })

    it('sets the total supply upon deployment', function() {
        return DappToken.deployed().then(function(instance) {
            tokenInstance = instance;
            return tokenInstance.totalSupply();
        }).then(function(totalSupply) {
            assert.equal(totalSupply.toNumber(), 100000, "total Supply");
            return tokenInstance.balanceOf(accounts[0]);
        }).then(function(adminBalance) {
            assert.equal(adminBalance.toNumber(), 100000, "all balance");
        });
    })

    it('transfers token ownership', function() {
        return DappToken.deployed().then(function(instance){
            tokenInstance = instance;
            return tokenInstance.transfer.call(accounts[1], 9999999999999999);
        }).then(assert.fail).catch(function(error){
            assert(error.message, 'error message must contain revert');
            return tokenInstance.transfer.call(accounts[1], 250000, {from: accounts[0] });
        }).then(function(success) {
            assert(success, true, 'it returns true');
            return tokenInstance.transfer(accounts[1], 250000, { from: accounts[0] });
        }).then(function(receipt) {
            assert.equal(receipt.logs.length, 1, 'triggers one event');
            assert.equal(receipt.logs[0].event, 'Transfer', 'should be the "Transfer" event');
            assert.equal(receipt.logs[0].args._from, accounts[0], 'logs the account the tokens are transferred from');
            assert.equal(receipt.logs[0].args._to, accounts[1], 'logs the account the tokens are transferred to');
            assert.equal(receipt.logs[0].args._value, 250000, 'logs the transfer amount');
            return tokenInstance.balanceOf(accounts[1])
        }).then(function(reciept) {
            return tokenInstance.balanceOf(accounts[1]);
        }).then(function(balance){
            assert.equal(balance.toNumber(), 250000, 'adds the amount to the recieving amount');
            return tokenInstance.balanceOf(accounts[0]);
        }).then(function(balance){
            assert.equal(balance.toNumber(), 999750000, 'deducts the amount from the sending account');
        });
    });
})