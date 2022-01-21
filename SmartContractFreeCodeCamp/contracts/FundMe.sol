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
    struct msg_info {
        address sender;
        uint256 value;
    }

    mapping(address => uint256) public addressToAmountFunded;
    uint256 public stored_value;

    // payable allows function to receive ether
    function fund() public payable {
        // $50
        // We are setting the minimum amount can sender
        uint256 minimumUSD = 50 * 10 ** 16;
        // require(1 > 0, abi.encodePacked(msg.sender));
        // This stops the transaction from happening. User's money
        // is not used and returned and also any unspent gas.
        require(getConversionRate(msg.value) >= minimumUSD, " You "
                    "need to spend more ETH");
        // amount sent by whoever calls this contract
        addressToAmountFunded[msg.sender] += msg.value;
        // what the ETH -> USD conversion rate is?
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
}