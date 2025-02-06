# scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from models import db, Alert
import requests
from config import Config
import telegram

# Переменная для хранения ссылки на приложение Flask
scheduler_app = None

def check_alerts():
    with scheduler_app.app_context():
        alerts = Alert.query.filter_by(active=True).all()
        for alert in alerts:
            portfolio = alert.portfolio
            coin_id = portfolio.asset_name.lower()
            url = f"{Config.COINGECKO_API_URL}/simple/price"
            params = {'ids': coin_id, 'vs_currencies': 'usd'}
            try:
                response = requests.get(url, params=params)
                data = response.json()
                current_price = data.get(coin_id, {}).get('usd', None)
                if current_price is None:
                    continue
                # Проверка условий уведомления
                if alert.alert_type == 'rise' and current_price >= alert.threshold_price:
                    send_telegram_notification(portfolio, current_price, alert)
                    alert.active = False  # деактивируем уведомление после срабатывания
                elif alert.alert_type == 'drop' and current_price <= alert.threshold_price:
                    send_telegram_notification(portfolio, current_price, alert)
                    alert.active = False
                db.session.commit()
            except Exception as e:
                print("Ошибка проверки уведомлений:", e)

def send_telegram_notification(portfolio, current_price, alert):
    message = (
        f"Сработало уведомление для {portfolio.asset_name}!\n"
        f"Текущая цена: {current_price} USD\n"
        f"Порог: {alert.threshold_price} USD"
    )
    try:
        bot = telegram.Bot(token=Config.TELEGRAM_TOKEN)
        bot.send_message(chat_id=Config.TELEGRAM_CHAT_ID, text=message)
    except Exception as e:
        print("Ошибка отправки сообщения в Telegram:", e)

def start_scheduler(app):
    global scheduler_app
    scheduler_app = app
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=check_alerts, trigger="interval", minutes=5)
    scheduler.start()
    
    # Останавливаем планировщик при завершении работы приложения
    import atexit
    atexit.register(lambda: scheduler.shutdown())
