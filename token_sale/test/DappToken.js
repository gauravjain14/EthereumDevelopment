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
            return tokenInstance.transfer.call(accounts[1], 99999999999999);
        }).then(assert.fail).catch(function(error){
            assert(error.message.indexOf('revert') >= 0, 'error message must contain revert');
            return tokenInstance.transfer.call(accounts[1], 25000, { from: accounts[0] });
            //return tokenInstance.transfer.call(accounts[1], 25000, { from: accounts[0] });
        }).then(function(success) {
            assert(success, true, 'it returns true');
            return tokenInstance.transfer(accounts[1], 25000, { from: accounts[0] });
        }).then(function(receipt) {
            assert.equal(receipt.logs.length, 1, 'triggers one event');
            assert.equal(receipt.logs[0].event, 'Transfer', 'should be the "Transfer" event');
            assert.equal(receipt.logs[0].args._from, accounts[0], 'logs the account the tokens are transferred from');
            assert.equal(receipt.logs[0].args._to, accounts[1], 'logs the account the tokens are transferred to');
            assert.equal(receipt.logs[0].args._value, 25000, 'logs the transfer amount');
            return tokenInstance.balanceOf(accounts[1])
        }).then(function(reciept) {
            return tokenInstance.balanceOf(accounts[1]);
        }).then(function(balance){
            assert.equal(balance.toNumber(), 25000, 'adds the amount to the recieving amount');
            return tokenInstance.balanceOf(accounts[0]);
        }).then(function(balance){
            assert.equal(balance.toNumber(), 75000, 'deducts the amount from the sending account');
        });
    });

    it('approves tokens for delegated transfer', function() {
        return DappToken.deployed().then(function(instance) {
            tokenInstance = instance;
            return tokenInstance.approve.call(accounts[1], 25000);
        }).then(function(success) {
            assert.equal(success, true, 'approve sender to withdraw');
            return tokenInstance.approve(accounts[1], 100, { from: accounts[0] });
        }).then(function(receipt) {
            // receipt - What is received once the transaction is executed
            assert.equal(receipt.logs.length, 1, 'triggers 1 event');
            assert.equal(receipt.logs[0].event, 'Approval', 'should be an approval event');
            assert.equal(receipt.logs[0].args._owner, accounts[0], 'logs the account the tokens are authorized by');
            assert.equal(receipt.logs[0].args._spender, accounts[1], 'logs the account the tokens are authorized to');
            assert.equal(receipt.logs[0].args._value, 100, 'logs the amount transfer is authorized for');
            // using the getter function of allowance below.
            return tokenInstance.allowance(accounts[0], accounts[1]);
        }).then(function(allowance){
            assert.equal(allowance, 100, 'stores the allowance for delegated transfer');
        });
    });

    it('handles delegated transfer', function() {
        return DappToken.deployed().then(function(instance) {
            tokenInstance = instance;
            fromAccount = accounts[2];
            toAccount = accounts[3];
            spendingAccount = accounts[4];
            // Transfer some tokens to the fromAccount
            return tokenInstance.transfer(fromAccount, 100, {from: accounts[0]});
        }).then(function(receipt) {
            return tokenInstance.approve(spendingAccount, 100, {from: fromAccount});
        }).then(function(receipt) {
            // Try transfer something larger (than the sender's balance)
            return tokenInstance.transferFrom(fromAccount, toAccount, 1122334455, {from: spendingAccount});
        }).then(assert.fail).catch(function(error) {
            assert(error.message.indexOf('revert') >= 0, 'cannot transfer value larger than balance');
            return tokenInstance.transferFrom.call(fromAccount, toAccount, 20, {from: spendingAccount});
        }).then(function(success) {
            assert.equal(success, true, 'transferFrom passes');
            return tokenInstance.transferFrom(fromAccount, toAccount, 20, {from: spendingAccount});
        }).then(function(receipt) {
            return tokenInstance.balanceOf(fromAccount);
        }).then(function(balance) {
            assert.equal(balance.toNumber(), 80, 'updated amount, after transfer of the sender');
            return tokenInstance.balanceOf(toAccount);
        }).then(function(balance) {
            assert.equal(balance.toNumber(), 20, 'updated balance of the receiver');
            return tokenInstance.allowance(fromAccount, spendingAccount);
        }).then(function(allowance) {
            assert.equal(allowance, 80, 'deducts the allowance from spender');
        });
    });
})