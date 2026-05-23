import os
import json
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

DATA_FILE = 'data.json'
data = {}   # key-value хранилище

# 3. Настройка Flask-Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day"]          # a) общее ограничение для ВСЕХ маршрутов
)

def load_data():
    global data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

def save_data():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

load_data()

# 2. Маршруты

@app.route('/set', methods=['POST'])
@limiter.limit("10 per minute")   # b) дополнительный лимит 10 запросов в минуту только для /set
def set_value():
    global data
    if not request.is_json:
        return jsonify({"error": "JSON data required"}), 400
    
    req = request.get_json()
    key = req.get('key')
    value = req.get('value')
    
    if key is None:
        return jsonify({"error": "Key is required"}), 400
    
    # Преобразуем ключ в строку для безопасности
    key = str(key)
    data[key] = value
    save_data()
    
    return jsonify({
        "message": f"Key '{key}' set successfully",
        "key": key
    }), 201


@app.route('/get/<string:key>', methods=['GET'])
def get_value(key):
    if key in data:
        return jsonify({"key": key, "value": data[key]})
    return jsonify({"error": "Key not found"}), 404


@app.route('/delete/<string:key>', methods=['DELETE'])
@limiter.limit("10 per minute")   # b) дополнительный лимит 10 запросов в минуту только для /delete
def delete_value(key):
    global data
    if key in data:
        del data[key]
        save_data()
        return jsonify({"message": f"Key '{key}' deleted successfully"})
    return jsonify({"error": "Key not found"}), 404


@app.route('/exists/<string:key>', methods=['GET'])
def exists_value(key):
    return jsonify({
        "key": key,
        "exists": key in data
    })


if __name__ == '__main__':
    app.run(debug=True)