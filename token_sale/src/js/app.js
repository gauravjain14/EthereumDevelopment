var Web3 = require('web3');

const ethEnabled = async() => {
    if (window.ethereum) {
        const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
        window.web3 = new Web3(window.ethereum);
        return true;
    }
    return false;
}

var App = {
    web3Provider: null,
    contracts: {},
    loading: false,
    account: "0x0",
    accounts: null,
    tokenPrice: 1000000000000000000, // wei
    tokensSold: 0,
    tokensAvailable: 75000,

    init: function() {
        console.log("App initialized...");
        // return App.initWeb3();
        return App.getEthAccounts();
    },

    initWeb3: function() {
        if (typeof web3 !== "undefined") {
            // If a web3 instance is already provided by Meta Mask
            App.web3Provider = web3.currentProvider;
            web3 = new Web3(web3.currentProvider);
        } else {
            // Specify default instance if no web3 instance is provided
            App.web3Provider = new Web3.providers.HttpProvider('http://localhost:7545');
            web3 = new Web3(App.web3Provider);
        }

        return App.initContracts();
    },

    initContracts: function() {
        $.getJSON("DappTokenSale.json", function(dappTokenSale) {
            App.contracts.DappTokenSale = TruffleContract(dappTokenSale);
            App.contracts.DappTokenSale.setProvider(App.web3Provider);
            App.contracts.DappTokenSale.deployed().then(function(dappTokenSale) {
                console.log("Dapp Token Sale address: ", dappTokenSale.address);
            })
        }).done(function() {
            $.getJSON("DappToken.json", function(dappToken) {
                App.contracts.DappToken = TruffleContract(dappToken);
                App.contracts.DappToken.setProvider(App.web3Provider);
                App.contracts.DappToken.deployed().then(function(dappToken) {
                    console.log("Dapp Token address: ", dappToken.address)
                })
            });

            return App.render();
        });
    },

    getEthAccounts: async function() {
        if (window.ethereum) {
            const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
            App.accounts = accounts;
            App.account = accounts[0];
            window.web3 = new Web3(window.ethereum);
            return App.initWeb3();
        }
    },

    render: function() {
        if (App.loading) {
            return;
        }
        App.loading = true;
        var loader = $('#loader');
        var content = $('#content');

        loader.show();
        content.hide();

        var dappTokenInstance = null;
        var dappTokenSaleInstance = null;
        App.contracts.DappTokenSale.deployed().then(function(instance) {
            console.log("DappTokenSale deployed");
            dappTokenSaleInstance = instance;
            return dappTokenSaleInstance.tokenPrice();
        }).then(function(tokenPrice) {
            console.log("Received token price");
            App.tokenPrice = tokenPrice;
            $('.token-price').html(web3.fromWei(App.tokenPrice, "ether"));
            return dappTokenSaleInstance.tokensSold();
        }).then(function(tokenSold) {
            console.log("token sold");
            App.tokensSold = tokenSold.toNumber();
            $('.tokens-sold').html(App.tokensSold);
            $('.tokens-available').html(App.tokensAvailable);

            var progressPercent = (Math.ceil(App.tokensSold) / App.tokensAvailable) * 100;
            $('#progress').css('width', progressPercent + '%');

            App.contracts.DappToken.deployed().then(function(instance) {
                console.log("Dapp token deployed");
                dappTokenInstance = instance;
                return dappTokenInstance.balanceOf(App.account);
            }).then(function(balance) {
                console.log("dapp balance", balance.toNumber())
                $('.dapp-balance').html(balance.toNumber());

                App.loading = false;
                loader.hide();
                content.show();
            })
        })
    },

    buyTokens: function() {
        $('#content').hide();
        $('#loader').show();

        var numberOfTokens = $('#numberOfTokens').val();
        App.contracts.DappTokenSale.deployed().then(function(instance) {
            return instance.buyTokens(numberOfTokens, {
                from: App.account,
                value: numberOfTokens * App.tokenPrice
            });
        }).then(function(result) {
            console.log('Tokens bought... ', result);
            $('form').trigger('reset');
            $('.tokens-sold').html(numberOfTokens);
            $('#loader').hide();
            $('#content').show();
        })
    }
}

$(function() {
    $(window).on('load', function () {
        // ethEnabled();
        App.init();
   });
})