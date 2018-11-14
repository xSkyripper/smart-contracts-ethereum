pragma solidity ^0.4.17;

contract Payment {
	address[4] public payers;

	// Paying a bill
	function pay(uint billId) public returns (uint) {
	  require(billId >= 0 && billId <= 3);

	  payers[billId] = msg.sender;

	  return billId;
	}
	
	// Retrieving the payers
	function getPayers() public view returns (address[4]) {
	  return payers;
	}
}
