// An NFT contract
// Mint one out of muliple dogs


// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase {
    uint256 public tokenCounter;
    bytes32 public keyhash;
    uint256 public fee;
    enum Breed{PUG, SHIBA_INU, ST_BERNARD}
    mapping(uint256 => Breed) public tokenIdToBreed;
    mapping(bytes32 => address) public requestIdToSender;
    event requestedCollectible(bytes32 indexed requestId, address requester);
    event breedAssigned (uint256 indexed tokenId, Breed breed);

    constructor(address _vrfCoordinator,
                address _linkToken,
                bytes32 _keyHash,
                uint256 _fee) public VRFConsumerBase(_vrfCoordinator, _linkToken)
                ERC721("Dogie", "DOG")
    {
        tokenCounter = 0;
        keyhash = _keyHash;
        fee = _fee;
    }

    function createCollectible() public returns (bytes32) {
        bytes32 requestId = requestRandomness(keyhash, fee);
        requestIdToSender[requestId] = msg.sender;
        emit requestedCollectible(requestId, msg.sender);
    }

    function _setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(_isApprovedOrOwner(msg.sender, tokenId), "ERC721: transfer caller is not owner nor approved");
        // _tokenURIs[tokenId] = tokenURI;
        _setTokenURI(tokenId, _tokenURI);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal 
        override 
    {
        require(_randomness > 0, "randomness not found");
        uint256 indeOxDog = _randomness % 3;
        Breed breed = Breed(indeOxDog);
        uint256 newTokenId = tokenCounter;
        tokenIdToBreed[newTokenId] = breed;
        emit breedAssigned(newTokenId, breed);
        // Now to mint, we need to figure out the original caller because
        // the msg.sender to fulfillRandomness is the VRFCoordinator.
        address owner = requestIdToSender[_requestId];
        _safeMint(owner, newTokenId);
        tokenCounter = tokenCounter + 1;
    }
}
