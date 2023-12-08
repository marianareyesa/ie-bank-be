from iebank_api.models import Account
import pytest

def test_create_account():
    """
    GIVEN a Account model
    WHEN a new Account is created
    THEN check the name, account_number, balance, currency, status and created_at fields are defined correctly
    """
    account = Account('John Doe', '€', 'Spain', '1234')
    assert account.name == 'John Doe'
    assert account.currency == '€'
    assert account.account_number != None
    assert account.balance == 0.0
    assert account.status == 'Active'
    assert account.country == 'Spain'
    assert account.password == '1234'

def test_account_initial_balance():
    """
    GIVEN an Account model
    WHEN a new Account is created without specifying an initial balance
    THEN the initial balance should be set to 0.0
    """
    account = Account('John Doe', '$', 'Spain', '1234')
    assert account.balance == 0.0

def test_account_update_balance():
    """
    GIVEN an Account model
    WHEN the balance of an Account is updated
    THEN the updated balance should be reflected correctly
    """
    account = Account('John Doe', '$', 'Spain','1234')
    # Set an initial balance
    account.balance = 100.0
    assert account.balance == 100.0

    # Update the balance
    account.balance += 100.0
    assert account.balance == 200.0

    # Deduct an amount from the balance
    account.balance -= 100.0
    assert account.balance == 100.0