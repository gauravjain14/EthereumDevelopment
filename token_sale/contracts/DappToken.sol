pragma solidity ^0.5.16;

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

    event Approval(
        address indexed _owner,
        address indexed _spender,
        uint256 _value
    );

    // rather than create a balanceOf function, define a variable that gets
    // its own setter/getter
    // gives a return function like function balanceOf(address _owner) {
    //  returns balance;   
    // }
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

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

    // approve
    function approve(address _spender, uint256 _value) public returns (bool success) {
        // Balance of the approver should be greater than value being approved for
        require(balanceOf[msg.sender] >= _value);

        allowance[msg.sender][_spender] = _value;

        // approve event
        emit Approval(msg.sender, _spender, _value);

        return true; 
    }

    // once approved, transfer
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        require(balanceOf[_from] >= _value);
        require(allowance[_from][msg.sender] >= _value);
        // change amounts

        // call a transfer event
        emit Transfer(_from, _to, _value);

        // Update the balance
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        allowance[_from][msg.sender] -= _value;

        return true;
    }
}