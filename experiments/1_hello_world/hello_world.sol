pragma solidity >=0.4.0 <0.6.0;

contract Mortal {
    address owner;

    constructor() public {
        owner = msg.sender;
    }

    function kill() public {
        if (msg.sender == owner) {
            selfdestruct(owner);
        }
    }
}

contract Greeter is Mortal {
    string greeting;

    constructor() public {
        greeting = "Basic greeting";
    }

    function setGreeting(string _greeting) public {
        greeting = _greeting;
    }

    function greet() public view returns (string) {
        return greeting;
    }
}