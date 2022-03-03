// SPDX-License-Identifier: MIT
pragma solidity ^0.7.1;

import "@chainlink/contracts/src/v0.7/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.7/VRFConsumerBase.sol";

contract Lottery is VRFConsumerBase, Ownable {

    // We make the array players payable because we need to deposit ETH
    address payable[] public players;
    address payable public lastPlayer;
    address payable public recentWinner;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed; // pulled from Chainlink
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    LOTTERY_STATE public lottery_state;
    uint256 public fee;
    bytes32 public keyhash;
    event RequestedRandomness(
        bytes32 requestId
    );

    // add vrfconsumerbase() to call the blockchain we are on.
    constructor(address _priceFeedAddress,
                address _vrfCoordinator, 
                address _link,
                uint256 _fee,
                bytes32 _keyhash) 
                        public VRFConsumerBase(_vrfCoordinator, _link) {
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        usdEntryFee = 50 * (10**18);
        lottery_state = LOTTERY_STATE.CLOSED;
        fee = _fee;
        keyhash = _keyhash;
    }

    function enter() public payable {
        // Add a condition for a minimum fees to enter
        require(lottery_state == LOTTERY_STATE.OPEN, "Lottery is not open yet");
        require(
            msg.value >= getEntranceFees(),
            "Not enough entrance fees ");
        players.push(msg.sender);
        lastPlayer = msg.sender;
    }

    function getEntranceFees() public view returns (uint256) {
        (,int256 price,,,) = ethUsdPriceFeed.latestRoundData();
        // price value returned contains 8 decimals
        uint256 adjustedPrice = uint256(price) * 10**10; // 18 decimals - Wei
        uint256 costToEnter = (usdEntryFee * 10**18) / adjustedPrice;

        return costToEnter;
    }

    function startLottery() public onlyOwner {
        require(lottery_state == LOTTERY_STATE.CLOSED, "can't start new lottery yet!");
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner {
        require(lottery_state == LOTTERY_STATE.OPEN, "Need the lottery to be open");

        // this is unacceptable since this can be easily manipulated by the miners.
        /* uint256(
            keccak256( // hashing algorithm
                abi.encodePacked(
                    nonce, // predictable since it's the transaction number
                    msg.sender, // msg.sender is predictable
                    block.difficulty, // not random; can be manipulated by miners!
                    block.timestamp
                );
            )
        ) % players.length; */

        // Chainlink VRF provides Verifiable Randomness
        // It doesn't immediately return the random number. It sends the request
        // offchain which when completed calls a callback function, which is
        // the fulfullRandomness function. So we need to override that.
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        bytes32 requestId = requestRandomness(keyhash, fee);

        // Emit an event to capture the return - 
        // they are like the print statement of a blockchain
        emit RequestedRandomness(requestId);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal 
        override 
    {
        require(lottery_state == LOTTERY_STATE.CALCULATING_WINNER,
                            "Need the lottery to be in calculating winner");
        require(_randomness > 0, "randomness not found");
        uint256 indexOfWinner = _randomness % players.length;

        recentWinner = players[indexOfWinner];
        recentWinner.transfer(address(this).balance);

        players = new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSED;
    }
}