pragma solidity ^0.4.17;

import "truffle/Assert.sol";
import "truffle/DeployedAddresses.sol";
import "../contracts/Payment.sol";

contract TestPayment {
    Payment payment = Payment(DeployedAddresses.Payment());
    uint expectedBillId = 2;

    address expectedPayer = this;

    // Test that when bill i is payed, confirmation for bill i is received
    function testUserCanPayBill() public {
        uint returnedId = payment.pay(expectedBillId);
        Assert.equal(returnedId, expectedBillId, "Payment of the expected bill should match what is returned.");
    }

    // Test that after paying a bill you become the owner of it 
    function testGetPayerAddressByBillId() public {
        address payer = payment.payers(expectedBillId);
        Assert.equal(payer, expectedPayer, "Owner of the expected bill should be this contract");
    }

    // Test that after paying a bill you become the owner of it using the getter 
    function testGetPayerAddressByBillIdInArray() public {
        address[4] memory payers = payment.getPayers();
        Assert.equal(payers[expectedBillId], expectedPayer, "Owner of the expected bill should be this contract");
    }

}