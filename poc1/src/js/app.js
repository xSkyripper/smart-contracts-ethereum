App = {
    web3Provider: null,
    contracts: {},

    init: async function() {
        // Load pets.
        $.getJSON('../bills.json', function(data) {
            var billsRow = $('#billRow');
            var billTemplate = $('#billTemplate');

            for (i = 0; i < data.length; i++) {
                billTemplate.find('.panel-title').text(data[i].name);
                billTemplate.find('img').attr('src', data[i].picture);
                billTemplate.find('.service').text(data[i].service);
                billTemplate.find('.due_date').text(data[i].due_date);
                billTemplate.find('.location').text(data[i].location);
                billTemplate.find('.btn-pay').attr('data-id', data[i].id);

                billsRow.append(billTemplate.html());
            }
        });

        return await App.initWeb3();
    },

    initWeb3: async function() {
        if (window.ethereum) {
            App.web3Provider = window.ethereum;
            try {
                // Request account access
                await window.ethereum.enable();
            } catch (error) {
                // User denied account access...
                console.error("User denied account access")
            }
        }
        // Legacy dapp browsers...
        else if (window.web3) {
            App.web3Provider = window.web3.currentProvider;
        }
        // If no injected web3 instance is detected, fall back to Ganache
        else {
            App.web3Provider = new Web3.providers.HttpProvider('http://localhost:7545');
        }
        web3 = new Web3(App.web3Provider);

        return App.initContract();
    },

    initContract: function() {
        $.getJSON('Payment.json', function(data) {
            // Get the necessary contract artifact file and instantiate it with truffle-contract
            var PaymentArtifact = data;
            App.contracts.Payment = TruffleContract(PaymentArtifact);

            // Set the provider for our contract
            App.contracts.Payment.setProvider(App.web3Provider);

            // Use our contract to retrieve and mark the adopted pets
            return App.markPayed();
        });
        return App.bindEvents();
    },

    bindEvents: function() {
        $(document).on('click', '.btn-pay', App.handlePay);
    },

    markPayed: function(payers, account) {
        var paymentInstance;

        App.contracts.Payment.deployed().then(function(instance) {
            paymentInstance = instance;

            return paymentInstance.getPayers.call();
        }).then(function(payers) {
            for (i = 0; i < payers.length; i++) {
                if (payers[i] !== '0x0000000000000000000000000000000000000000') {
                    $('.panel-pet').eq(i).find('button').text('Success').attr('disabled', true);
                }
            }
        }).catch(function(err) {
            console.log(err.message);
        });
    },

    handlePay: function(event) {
        event.preventDefault();

        var billId = parseInt($(event.target).data('id'));
        var paymentInstance;

        web3.eth.getAccounts(function(error, accounts) {
            if (error) {
                console.log(error);
            }

            var account = accounts[0];

            App.contracts.Payment.deployed().then(function(instance) {
                paymentInstance = instance;

                // Execute pay as a transaction by sending account
                return paymentInstance.pay(billId, {
                    from: account
                });
            }).then(function(result) {
                return App.markPayed();
            }).catch(function(err) {
                console.log(err.message);
            });
        });
    }

};

$(function() {
    $(window).load(function() {
        App.init();
    });
});