var DappToken = artifacts.require("DappToken.sol");
var DappTokenSale = artifacts.require("./DappTokenSale.sol");

module.exports = function (deployer) {
  deployer.deploy(DappToken, 'DApp Token', 100000, 'DApp').then(function() {
    var tokenPrice = web3.utils.toWei("1.0", "ether");
    return deployer.deploy(DappTokenSale, DappToken.address, tokenPrice);
  });
};
