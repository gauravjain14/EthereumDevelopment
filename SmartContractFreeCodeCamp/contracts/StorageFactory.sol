// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

import "./1_Storage.sol";

contract StorageFactory is Storage {
    Storage[] public storageArray;

    function createStorageFactoryContract() public {
        Storage simpleStorage = new Storage();
        storageArray.push(simpleStorage);
    }

    // Remove all the functions and make this class inherit from Storage class 
    /* function storeNumber(uint256 _index, uint256 _number) public{
        // we need to retrieve the contract. 
        // but can we not directly use storageArray[_index]?
        storageArray[_index].store(_number);
    }

    // both are same
    function retrieveStorage(uint256 _index) view public returns(uint256) {
        return storageArray[_index].retrieve();
    } */
}