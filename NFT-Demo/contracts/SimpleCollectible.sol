// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

/*
// ERC721 reference
interface ERC721 {
    balanceOf(owner)
    ownerOf(tokenId)
    safeTransferFrom(from, to, tokenId)
    transferFrom(from, to, tokenId)
    approve(to, tokenId)
    getApproved(tokenId)
    setApprovalForAll(operator, _approved)
    isApprovedForAll(owner, operator)
    safeTransferFrom(from, to, tokenId, data)
}
*/

contract SimpleCollectible is ERC721 {
    uint256 public tokenCounter;
    mapping (uint256 => string) public _tokenURIs;

    constructor() public ERC721 ("Doggie", "DOG") {
        tokenCounter = 0;
    }

    function _setTokenURI(uint256 tokenId, string memory tokenURI) public {
        _tokenURIs[tokenId] = tokenURI;
    }

    function _baseURI() internal view override returns (string memory) {
        return "";
    }

    function createCollectible(string memory tokenURI) public returns (uint256) {
        uint256 newTokenId = tokenCounter;
        _safeMint(msg.sender, newTokenId); // nft-owner and tokenId
        _setTokenURI(newTokenId, tokenURI);
        tokenCounter += 1;
        return newTokenId;
    }
}