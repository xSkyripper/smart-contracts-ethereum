pragma solidity ^0.4.24;

contract Payment {
    struct Payer {
        address addr;
        bool payed;  
    }
    
    address owner;
    uint amountDue;
    Payer[] payers;

    constructor(uint _amountDue) public {
        amountDue = _amountDue;
        owner = msg.sender;
    }

    modifier onlyOwner  {
        require(msg.sender == owner, "Only owner can call this function.");
        _;
    }

    function close() public onlyOwner {
        selfdestruct(owner);
    }


    function addPayer(address _payerAddr) public onlyOwner {
        for (uint payerIdx = 0; payerIdx < payers.length; payerIdx++) {
            require(!(payers[payerIdx].addr == _payerAddr), "Already added!");
        }

        Payer memory payer = Payer({
            addr: _payerAddr,
            payed: false
            });
        
        payers.push(payer);
    }

    function getPayers() public view onlyOwner returns (address[] memory) {
        address[] memory payersAddresses;
        return payersAddresses;
    }


    function pay(uint billId) public payable returns (uint) {
        for (uint payerIdx = 0; payerIdx < payers.length; payerIdx++) {
            if (payers[payerIdx].addr == msg.sender) {
                require(!payers[payerIdx].payed, "Already payed!");
                payers[payerIdx].payed = true;
            }
        }

        return billId;
    }
	
    function getAmountDue() public view returns (uint) {
        return amountDue;
    }

    function getContractBalance() public onlyOwner returns (uint){
        return address(this).balance;
    }
}
