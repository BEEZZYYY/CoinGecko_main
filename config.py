# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///crypto_portfolio.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    COINGECKO_API_URL = "https://api.coingecko.com/api/v3"
    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN') or '7775876227:AAFz7BWKoJnc56V9K2fpfBgjEH4WHgZTBr0'
    TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID') or '7292201215'
