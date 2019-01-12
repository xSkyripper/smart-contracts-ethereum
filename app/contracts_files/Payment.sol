pragma solidity ^0.4.24;

contract Payment {
    struct PayerData {
        bool payed;
        bool exists;
    }
    
    address owner;
    uint amountDue;
    
    address[] payersList;
    mapping (address => PayerData) payers;

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
        require(payers[_payerAddr].exists == false, "Payer already exists!");

        PayerData memory newPayerData = PayerData({
            payed: false,
            exists: true
        });

        payers[_payerAddr] = newPayerData;
        payersList.push(_payerAddr);
    }

    function getPayers() public view returns (address[] memory) {
        return payersList;
    }

    function removePayer(address _payerAddr) public onlyOwner {
        require(payers[_payerAddr].exists == true, "Payer doesn't exist!");

        delete payers[_payerAddr];

        uint indexToDelete;
        for (uint payerIdx = 0; payerIdx < payersList.length; payerIdx++) {
            if (payersList[payerIdx] == _payerAddr) {
                indexToDelete = payerIdx;
                break;
            }
        }

        if (payersList.length > 1) {
            payersList[indexToDelete] = payersList[payersList.length - 1];
        }
        payersList.length--;
    }

    function pay() public payable returns (uint) {
        require(payers[msg.sender].exists, "The payer is not in this contract!");
        require(!payers[msg.sender].payed, "The payer has already payed!");
        require(msg.value == amountDue, "Incorrect amount payed!");

        payers[msg.sender].payed = true;
    }

    function getAmountDue() public view returns (uint) {
        return amountDue;
    }

    function checkPaymentStatus(address _payerAddr) public view returns (bool) {
        require(msg.sender == _payerAddr || msg.sender == owner, "You cannot check someone else's payment status");

        return payers[_payerAddr].payed;
    }

    function getContractBalance() public onlyOwner returns (uint){
        return address(this).balance;
    }
}
