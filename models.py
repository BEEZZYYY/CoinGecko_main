# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    portfolios = db.relationship('Portfolio', backref='user', lazy=True)

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Если авторизация не реализована, можно оставить user_id как опциональный
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    asset_symbol = db.Column(db.String(10), nullable=False)
    asset_name = db.Column(db.String(50), nullable=False)  # например, 'bitcoin'
    quantity = db.Column(db.Float, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    transactions = db.relationship('Transaction', backref='portfolio', lazy=True)
    alerts = db.relationship('Alert', backref='portfolio', lazy=True)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), nullable=False)
    transaction_type = db.Column(db.String(10))  # "buy" или "sell"
    date = db.Column(db.DateTime, default=datetime.utcnow)
    quantity = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), nullable=False)
    threshold_price = db.Column(db.Float, nullable=False)
    alert_type = db.Column(db.String(10))  # "rise" (рост) или "drop" (падение)
    active = db.Column(db.Boolean, default=True)
