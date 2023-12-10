from iebank_api.models import Account, Transaction
from iebank_api import app, db #to test the login
import json #testing login
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
    assert account.balance == 1000.0
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
    assert account.balance == 1000.0

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

#Unit tests for transactions

def test_create_transaction():
    """
    GIVEN a Transaction model
    WHEN a new Transaction is created
    THEN check the sender_id, receiver_id, and amount fields are defined correctly
    """
    sender = Account('Sender', '€', 'Spain', 'password')
    receiver = Account('Receiver', '€', 'Spain', 'password')
    transaction = Transaction(sender.id, receiver.id, 500.0)
    assert transaction.sender_id == sender.id
    assert transaction.receiver_id == receiver.id
    assert transaction.amount == 500.0

def test_transaction_amount():
    """
    GIVEN a Transaction model
    WHEN a new Transaction is created with an amount
    THEN check if the amount transferred is subtracted from the sender's balance and added to the receiver's balance
    """
    sender_initial_balance = 1000.0
    receiver_initial_balance = 1000.0
    amount_transferred = 500.0

    sender = Account('Sender', '€', 'Spain', 'password')
    sender.balance = sender_initial_balance

    receiver = Account('Receiver', '€', 'Spain', 'password')
    receiver.balance = receiver_initial_balance

    transaction = Transaction(sender.id, receiver.id, amount_transferred)
    sender.balance -= amount_transferred
    receiver.balance += amount_transferred

    assert sender.balance == sender_initial_balance - amount_transferred
    assert receiver.balance == receiver_initial_balance + amount_transferred


#Unit tests for log in
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client: #creating client
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all() #remove dummy client after testing

def test_correct_login(client):
    # Create a test account
    test_account = Account('Test User', '€', 'Spain', 'password')
    db.session.add(test_account)
    db.session.commit()

    # Send a login request with correct credentials
    response = client.post('/userlogin', json={'name': 'Test User', 'password': 'password'})
    data = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert 'id' in data
    assert 'name' in data
    assert 'balance' in data  # Assuming you want to return some account data upon successful login

def test_failed_login(client):
    # Create a test account
    test_account = Account('Test User', '€', 'Spain', 'password')
    db.session.add(test_account)
    db.session.commit()

    # Send a login request with incorrect credentials
    response = client.post('/userlogin', json={'name': 'Test User', 'password': 'wrong_password'})

    assert response.status_code == 200  # Assuming you return a 200 status even for failed login attempts
    assert b'Wrong credentials' in response.data