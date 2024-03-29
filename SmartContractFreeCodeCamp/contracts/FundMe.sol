// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

// Chainlink is a decentralized oracle network.
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
// SafeMathChainlink is not in 0.8 onwards;
// import "@chainlink/contracts/src/v0.7/vendor/SafeMathChainlink.sol";

// Couple of learnings point - to import an library we need to
// mention the datatype we would the library for.
// using Library as DataType;
// using Lirbary as *; -- we can use the library for any DataType 

contract FundMe {
    // using SafeMathChainlink for uint256;

    address owner_;
    mapping(address => uint256) public addressToAmountFunded;
    // multiple addresses can call this contract to deposit funds. We need to
    // keep a track of all the funders.
    address[] public funders;
    
    constructor() public {
        // owner will be the address that deploys this contract.
        owner_ = msg.sender;
    }

    // payable allows function to receive ether
    function fund() public payable {
        // $50
        // We are setting the minimum amount can sender
        uint256 minimumUSD = 50 * 10 ** 16;
        // This stops the transaction from happening. User's money
        // is not used and returned and also any unspent gas.
        require(getConversionRate(msg.value) >= minimumUSD, " You "
                    "need to spend more ETH");
        // amount sent by whoever calls this contract
        addressToAmountFunded[msg.sender] += msg.value;
        // Update the funders list
        funders.push(msg.sender);
    }

    function retrieveFund() view public returns(uint256) {
        return addressToAmountFunded[msg.sender];
    }

    // override the function belonging to the AggregatorV3Interface
    function version() external view returns (uint256) {
        // address at which the smart contract is located is required to get an
        // instance to the smart contract.
        // We are using the ETH/USD price feed on the Rinkeby Test network.
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
        return priceFeed.version();
    }

    // We don't need to implement the interface. Right?
    function getPrice() public view returns(uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
        // One way of returning the struct from function calls
        /* (
            uint80 roundID, 
            int price,
            uint startedAt,
            uint timeStamp,
            uint80 answeredInRound
        ) = priceFeed.latestRoundData(); */
        (,int price,,,) = priceFeed.latestRoundData();
        return uint256(price * 1000000000); // convert from Gwei to Wei
    }

    function getConversionRate(uint256 ethAmount) public returns(uint256) {
        uint256 ethPrice = getPrice(); // in Wei
        uint256 ethAmountInUSD = (ethPrice * ethAmount) / 1000000000000000000; // still remains in Wei
        return ethAmountInUSD; // in Wei
    }

    // modifier runs the require first;
    modifier onlyOwner {
        require(msg.sender == owner_);
        _;
    }

    function withdraw() payable onlyOwner public {
        // https://stackoverflow.com/questions/68545930/how-to-withdraw-all-tokens-from-the-my-contract-in-solidity#:~:text=To%20withdraw%20a%20token%20balance,you%20pass%20as%20an%20input.
        payable(msg.sender).transfer(address(this).balance);
        // reset everyone's balance to zero
        for (uint256 funderIndex = 0; funderIndex < funders.length; funderIndex++) {
            addressToAmountFunded[funders[funderIndex]] = 0;
        }

        funders = new address[](0); // reset funders array as well
    }
}