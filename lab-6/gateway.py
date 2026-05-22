from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

# Адреса других микросервисов
CURRENCY_URL = "http://localhost:5001"
DATA_URL = "http://localhost:5002"

# Главная страница (frontend)
@app.route("/", methods=["GET", "POST"])
def index():
    message = None

    if request.method == "POST":
        action = request.form.get("action")

        if action == "load":
            resp = requests.post(f"{CURRENCY_URL}/load", json={
                "currency_name": request.form.get("currency_name", "").upper(),
                "rate": float(request.form.get("rate", 0))
            })
            message = resp.json().get("message") or resp.json().get("error")

        elif action == "update":
            resp = requests.post(f"{CURRENCY_URL}/update_currency", json={
                "currency_name": request.form.get("currency_name", "").upper(),
                "rate": float(request.form.get("rate", 0))
            })
            message = resp.json().get("message") or resp.json().get("error")

        elif action == "delete":
            resp = requests.post(f"{CURRENCY_URL}/delete", json={
                "currency_name": request.form.get("currency_name", "").upper()
            })
            message = resp.json().get("message") or resp.json().get("error")

        elif action == "convert":
            resp = requests.get(f"{DATA_URL}/convert", params={
                "currency_name": request.form.get("currency_name", "").upper(),
                "amount": request.form.get("amount")
            })
            if resp.status_code == 200:
                result = resp.json()
                message = f"{result['amount']} {result['currency']} = {result['converted_to_rub']} RUB"
            else:
                message = resp.json().get("error", "Ошибка")

    # Получаем список валют
    currencies = []
    try:
        resp = requests.get(f"{DATA_URL}/currencies")
        if resp.status_code == 200:
            currencies = resp.json()
    except:
        pass

    return render_template("index.html", currencies=currencies, message=message)


# Прокси для всех остальных запросов (если frontend будет использовать API напрямую)
@app.route("/load", methods=["POST"])
def proxy_load():
    resp = requests.post(f"{CURRENCY_URL}/load", json=request.get_json())
    return jsonify(resp.json()), resp.status_code

@app.route("/update_currency", methods=["POST"])
def proxy_update():
    resp = requests.post(f"{CURRENCY_URL}/update_currency", json=request.get_json())
    return jsonify(resp.json()), resp.status_code

@app.route("/delete", methods=["POST"])
def proxy_delete():
    resp = requests.post(f"{CURRENCY_URL}/delete", json=request.get_json())
    return jsonify(resp.json()), resp.status_code

@app.route("/convert", methods=["GET"])
def proxy_convert():
    resp = requests.get(f"{DATA_URL}/convert", params=request.args)
    return jsonify(resp.json()), resp.status_code

@app.route("/currencies", methods=["GET"])
def proxy_currencies():
    resp = requests.get(f"{DATA_URL}/currencies")
    return jsonify(resp.json()), resp.status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)