const DappToken = artifacts.require("DappToken.sol");

module.exports = function (deployer) {
  deployer.deploy(DappToken, 'DApp Token', 100000, 'DApp');
};
