from brownie import SimpleStorage, accounts

''' When running the tests, we can use brownie -s to print lines.
Brownie testing framework follows the pytest documentation'''

def test_deploy():
    # Divide the tests in three categories
    # Arrange
    account = accounts[0]
    # Act
    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.retrieve() # brownie uses Call
    expected = 0
    # Assert
    assert starting_value == expected

def test_updating_storage():
    print("Hello hello")
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    expected = 515
    simple_storage.store(expected, {"from": account})
    assert expected == simple_storage.retrieve()