# routes/portfolio.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Portfolio, Alert
import requests
from config import Config

portfolio_bp = Blueprint('portfolio', __name__)

@portfolio_bp.route('/')
def index():
    portfolios = Portfolio.query.all()
    # Получаем текущие цены для каждого актива через CoinGecko API
    prices = {}
    for p in portfolios:
        url = f"{Config.COINGECKO_API_URL}/simple/price"
        params = {
            'ids': p.asset_name.lower(),  # asset_name должен совпадать с id монеты в CoinGecko (например, bitcoin)
            'vs_currencies': 'usd'
        }
        try:
            response = requests.get(url, params=params)
            data = response.json()
            prices[p.id] = data.get(p.asset_name.lower(), {}).get('usd', 0)
        except:
            prices[p.id] = 0
    return render_template('portfolio.html', portfolios=portfolios, prices=prices)

@portfolio_bp.route('/add', methods=['GET', 'POST'])
def add_asset():
    if request.method == 'POST':
        asset_symbol = request.form.get('asset_symbol')
        asset_name = request.form.get('asset_name')
        quantity = float(request.form.get('quantity'))
        purchase_price = float(request.form.get('purchase_price'))
        new_asset = Portfolio(asset_symbol=asset_symbol, asset_name=asset_name, quantity=quantity, purchase_price=purchase_price)
        db.session.add(new_asset)
        db.session.commit()
        flash("Актив успешно добавлен!")
        return redirect(url_for('portfolio.index'))
    return render_template('add_asset.html')

@portfolio_bp.route('/set_alert/<int:portfolio_id>', methods=['GET', 'POST'])
def set_alert(portfolio_id):
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    if request.method == 'POST':
        threshold_price = float(request.form.get('threshold_price'))
        alert_type = request.form.get('alert_type')
        alert = Alert(portfolio_id=portfolio_id, threshold_price=threshold_price, alert_type=alert_type)
        db.session.add(alert)
        db.session.commit()
        flash("Уведомление установлено!")
        return redirect(url_for('portfolio.index'))
    return render_template('set_alert.html', portfolio=portfolio)

@portfolio_bp.route('/chart/<int:portfolio_id>')
def chart(portfolio_id):
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    # Для демонстрации создаем фиктивные исторические данные.
    # В реальном приложении можно получать исторические данные через API или сохранять их в БД.
    import random
    dates = ["2025-01-0"+str(i) for i in range(1,10)]
    prices = [portfolio.purchase_price + random.uniform(-10,10) for _ in range(len(dates))]
    return render_template('chart.html', portfolio=portfolio, dates=dates, prices=prices)
