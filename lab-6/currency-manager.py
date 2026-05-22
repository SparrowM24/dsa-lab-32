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

# Создаём таблицу при запуске
with db() as conn:
    conn.cursor().execute("""
        CREATE TABLE IF NOT EXISTS currencies (
            id SERIAL PRIMARY KEY,
            currency_name VARCHAR(10) UNIQUE NOT NULL,
            rate NUMERIC(15,6) NOT NULL
        )
    """)
    conn.commit()

@app.post("/load")
def load():
    data = request.get_json()
    name = data.get("currency_name", "").strip().upper()
    rate = data.get("rate")

    if not name or rate is None:
        return jsonify({"error": "Нужны currency_name и rate"}), 400
    
    if rate <= 0:
        return jsonify({"error": "Курс должен быть положительным числом"}), 400
    
    with db() as conn:
        cur = conn.cursor()
        # Проверка, что валюты нет
        cur.execute("SELECT 1 FROM currencies WHERE currency_name = %s", (name,))
        if cur.fetchone():
            return jsonify({"error": "Валюта уже есть"}), 409

        # Сохраняем
        cur.execute("INSERT INTO currencies (currency_name, rate) VALUES (%s, %s)",
                    (name, float(rate)))
        conn.commit()

    return jsonify({"message": "Валюта добавлена"}), 200


@app.post("/update_currency")
def update_currency():
    data = request.get_json()
    name = data.get("currency_name", "").strip().upper()
    rate = data.get("rate")

    if not name or rate is None:
        return jsonify({"error": "Нужны currency_name и rate"}), 400
    rate = float(rate)

    if rate <= 0:
        return jsonify({"error": "Курс должен быть положительным числом"}), 400
    
    with db() as conn:
        cur = conn.cursor()
        # 1. Проверяем, что валюта существует
        cur.execute("SELECT 1 FROM currencies WHERE currency_name = %s", (name,))
        if not cur.fetchone():
            return jsonify({"error": "Валюты нет в БД"}), 404

        # 2. Обновляем курс
        cur.execute("UPDATE currencies SET rate = %s WHERE currency_name = %s",
                    (float(rate), name))
        conn.commit()

    # 3. 200 OK
    return jsonify({"message": "Курс обновлён"}), 200


@app.post("/delete")
def delete_currency():
    data = request.get_json()
    name = data.get("currency_name", "").strip().upper()

    if not name:
        return jsonify({"error": "Нужно currency_name"}), 400

    with db() as conn:
        cur = conn.cursor()
        # 1. Проверяем, что валюта существует
        cur.execute("SELECT 1 FROM currencies WHERE currency_name = %s", (name,))
        if not cur.fetchone():
            return jsonify({"error": "Валюты нет в БД"}), 404

        # 2. Удаляем
        cur.execute("DELETE FROM currencies WHERE currency_name = %s", (name,))
        conn.commit()

    # 3. 200 OK
    return jsonify({"message": "Валюта удалена"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)