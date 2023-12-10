from iebank_api import db
from datetime import datetime
import string, random

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    account_number = db.Column(db.String(20), nullable=False, unique=True)
    balance = db.Column(db.Float, nullable=False, default = 1000.0)
    currency = db.Column(db.String(1), nullable=False, default="€")
    country = db.Column(db.String(32), nullable=False, default="Spain")
    status = db.Column(db.String(10), nullable=False, default="Active")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    password = db.Column(db.String(32), nullable=False)
    
  

    def __repr__(self):
        return '<Event %r>' % self.account_number

    def __init__(self, name, currency, country, password):
        self.name = name
        self.account_number = ''.join(random.choices(string.digits, k=20))
        self.currency = currency
        self.balance = 1000.0
        self.status = "Active"
        self.country = country
        self.password = password

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, nullable=False)
    receiver_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    
   

    def __repr__(self):
        return f'Transaction {self.id}'

    def __init__(self, sender_id, receiver_id, amount):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.amount = amount
    