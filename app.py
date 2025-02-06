# app.py
from flask import Flask
from config import Config
from models import db
from routes.portfolio import portfolio_bp
from routes.api import api_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Регистрация маршрутов (Blueprints)
app.register_blueprint(portfolio_bp)
app.register_blueprint(api_bp, url_prefix='/api')

# Создаем БД (если не существует)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # Запуск APScheduler для фоновых задач
    from scheduler import start_scheduler
    start_scheduler(app)
    app.run(debug=True)
