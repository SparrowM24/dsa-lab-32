from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Подключение к базе
def db():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )

@app.get("/convert")
def convert():
    currency = request.args.get("currency_name", "").strip().upper()
    amount_str = request.args.get("amount")

    if not currency or not amount_str:
        return jsonify({"error": "Нужны currency_name и amount"}), 400

    try:
        amount = float(amount_str)
    except:
        return jsonify({"error": "amount должен быть числом"}), 400

    with db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT rate FROM currencies WHERE currency_name = %s", (currency,))
        row = cur.fetchone()

        if not row:
            return jsonify({"error": "Валюты нет в БД"}), 404

        rate = float(row[0])
        converted = amount * rate

    # Возвращаем JSON с результатом
    return jsonify({
        "currency": currency,
        "amount": amount,
        "rate": rate,
        "converted_to_rub": round(converted, 2)
    }), 200


@app.get("/currencies")
def get_currencies():
    with db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, currency_name, rate FROM currencies ORDER BY currency_name")
        rows = cur.fetchall()

    # Возвращаем список всех валют
    currencies = [
        {"id": row[0], "currency_name": row[1], "rate": float(row[2])}
        for row in rows
    ]

    return jsonify(currencies), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)