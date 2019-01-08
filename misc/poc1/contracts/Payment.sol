pragma solidity ^0.4.17;

contract Payment {
	
	struct Payer {
	    address addr;
        bool payed;  // if true, that person already voted
    }
    
    Payer[] payers;
    uint amountDue;

    constructor() public {
        amountDue = 5;
    	payers.push(Payer({
    	addr: 0x6D4E5BAc0fc3fF8dF7A713DC0bB47cEF310a92cB,
    	payed: false
    	}));
    	payers.push(Payer({
    	addr: 0xeec7A4E837eEB5242E9d20976286a0cCD464EFb5,
    	payed: false
    	}));
    	payers.push(Payer({
    	addr: 0xe603AFeC589146C9A03786255b9386462EaeD9e5,
    	payed: true
    	}));

    }

	// Paying a bill
	function pay(uint billId) public payable returns (uint) {
	  for (uint p = 0; p < payers.length; p++) {
            if (payers[p].addr == msg.sender) {
      			require(!payers[p].payed, "Already payed!");
      			payers[p].payed = true;
            }
        }

	  return billId;
	}
	
	function getAmountDue() returns (uint){
		return amountDue;
	}

	// Retrieving the payers
	function getPayers() public view returns (address[]) {
	  address[] payers_addresses;
	  return payers_addresses;
	}
	function getContractBalance() public returns (uint){
	  return this.balance;
	}
}
