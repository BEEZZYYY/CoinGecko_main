# routes/api.py
from flask import Blueprint, jsonify, request
import requests
from config import Config

api_bp = Blueprint('api', __name__)

@api_bp.route('/price/<string:coin_id>', methods=['GET'])
def get_price(coin_id):
    # Пример вызова: GET /api/price/bitcoin
    url = f"{Config.COINGECKO_API_URL}/simple/price"
    params = {
        'ids': coin_id,
        'vs_currencies': 'usd'
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
