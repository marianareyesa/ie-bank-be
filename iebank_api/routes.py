from flask import Flask, jsonify,request
from iebank_api import db, app
from iebank_api.models import Account, Transaction
import json


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/skull', methods=['GET'])
def skull():
    text = 'Hi! This is the BACKEND SKULL! 💀 '
    text = text +'<br/>Database URL:' + db.engine.url.database
    if db.engine.url.host:
        text = text +'<br/>Database host:' + db.engine.url.host
    if db.engine.url.port:
        text = text +'<br/>Database port:' + db.engine.url.port
    if db.engine.url.username:
        text = text +'<br/>Database user:' + db.engine.url.username
    if db.engine.url.password:
        text = text +'<br/>Database password:' + db.engine.url.password
    return text


@app.route('/accounts', methods=['POST'])
def create_account():
    name = request.json['name']
    country = request.json['country']
    currency = request.json['currency']
    password = request.json['password']
    account = Account(name, currency, country, password)
    db.session.add(account)
    db.session.commit()
    return format_account(account)

@app.route('/accounts', methods=['GET'])
def get_accounts():
    accounts = Account.query.all()
    return {'accounts': [format_account(account) for account in accounts]}

@app.route('/accounts/<int:id>', methods=['GET'])
def get_account(id):
    account = Account.query.get(id)
    return format_account(account)

@app.route('/accounts/<int:id>', methods=['PUT'])
def update_account(id):
    account = Account.query.get(id)
    account.name = request.json['name']
    db.session.commit()
    return format_account(account)

@app.route('/accounts/<int:id>', methods=['DELETE'])
def delete_account(id):
    account = Account.query.get(id)
    db.session.delete(account)
    db.session.commit()
    return format_account(account)

@app.route('/userlogin', methods=['POST'])
def log_in():
    name = request.json['name']
    password = request.json['password']
    account = Account.query.filter_by(name = name).first()
    if account and name == account.name and password == account.password:
        return format_account(account)
    else:
        return 'Wrong credentials'

@app.route('/upage/<string:username>', methods=['GET'])
def get_user_by_username(username):
    account = Account.query.filter_by(name=username).first()
    print(account.name)
    if account:
        user_data = {
            'name': account.name,
            'accounts': [
                {
                    'id': account.id,
                    'balance': account.balance,
                    # Other account details
                }
            ]
        }
        return jsonify(user_data)
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/transaction', methods=['POST'])
def transaction_handler():
    name = request.json['name']
    amount= request.json['amount']
    amount= float(amount)
    receiver= request.json['receiver']
    print("***")
    print(name)
    print(amount)
    print(receiver)
    print("***")
    try:
        # Fetch sender's account
        sender_account = Account.query.filter_by(name=name).first()

        # Fetch receiver's account
        receiver_account = Account.query.filter_by(name=receiver).first()

        if sender_account is None or receiver_account is None:
            return jsonify({'message': 'Invalid sender or receiver'}), 404

        # Check if the sender has enough balance
        if sender_account.balance < amount:
            return jsonify({'message': 'Insufficient balance'}), 400

        # Perform the transaction
        sender_account.balance -= amount
        receiver_account.balance += amount
        db.session.commit()
        # Create a new transaction record
        transaction = Transaction(
            sender_id=sender_account.id,
            receiver_id=receiver_account.id,
            amount=amount
        )
        db.session.add(transaction)
        db.session.commit()

        # Add the transaction to sender's transactions
        

        # Update the database
        
        transactions = Transaction.query.filter(Transaction.sender_id == sender_account.id).all()
        
        # Print receiver's transactions
        
        
        transaction_data = []
        for transaction in transactions:
            sender = Account.query.get(transaction.sender_id)
            receiver = Account.query.get(transaction.receiver_id)
            transaction_data.append({
                'sender': sender.name,
                'receiver': receiver.name,
                'amount': transaction.amount,
            })

        # Return the list of transactions to the front end
        return jsonify({'message': 'Transaction successful', 'transactions': transaction_data})
    except Exception as e:
        # Handle any other exceptions
        print(str(e))
        return jsonify({'message': 'Error processing transaction'}), 500

@app.route('/transaction-history/<string:username>', methods=['GET'])
def get_transaction_history(username):
    sender_account = Account.query.filter_by(name=username).first()
    if sender_account:
        # Filter transactions where the sender is the specified user
        transactions = Transaction.query.filter_by(sender_id=sender_account.id).all()

        transaction_data = []
        for transaction in transactions:
            receiver = Account.query.get(transaction.receiver_id)
            transaction_data.append({
                'sender': username,
                'receiver': receiver.name,
                'amount': transaction.amount,
                # Include other relevant transaction details
            })

        return jsonify({'transactions': transaction_data})
    else:
        return jsonify({'message': 'User not found or no transactions'}), 404




def format_account(account):
    return {
        'id': account.id,
        'name': account.name,
        'account_number': account.account_number,
        'balance': account.balance,
        'currency': account.currency,
        'country': account.country,
        'status': account.status,
        'created_at': account.created_at,
        'password': account.password
    }