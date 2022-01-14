pragma solidity ;

// implement the ERC20 standard;
contract DappToken {
    // Name
    string public name;
    // symbol
    string public symbol;
    string public standard;
    
    // Set the total number of tokens
    // Read the total number of tokens
    uint256 public totalSupply;

    event Transfer(
        address indexed _from,
        address indexed _to,
        uint256 _value
    );

    // rather than create a balanceOf function, define a variable that gets
    // its own setter/getter
    // gives a return function like function balanceOf(address _owner) {
    //  returns balance;   
    // }
    mapping(address => uint256) public balanceOf;
     
    constructor(string memory _name, uint256 _initialSupply,
                                        string memory _symbol) public {
        name = _name;
        totalSupply = _initialSupply;
        // initiate balance
        // msg is an object consisting of several values, in Solidity
        balanceOf[msg.sender] = _initialSupply;
        //
        symbol = _symbol;
    }

    // Transfer function to trigger a transfer event on the network
    // return a boolean and if the account doesn't have enough, throw an 
    // exception
    function transfer(address _to, uint256 _value) public returns (bool success) {
        require(balanceOf[msg.sender] >= _value);

        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;

        emit Transfer(msg.sender, _to, _value);

        return true;
    }
}