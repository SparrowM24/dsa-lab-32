import random
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
OPERATIONS = ['sum', 'sub', 'mul', 'div']

# Раздел I. Подготовка сервера с API
@app.route('/number/', methods=['GET'])
def get_number():
    param = request.args.get('param', type=int)
    rand_val = random.randint(1, 100)
    number = rand_val * param
    operation = random.choice(OPERATIONS)
    return jsonify({"number": number, "operation": operation})


@app.route('/number/', methods=['POST'])
def post_number():
    data = request.get_json()   # читаем JSON
    json_param = int(data['jsonParam'])
    rand_val = random.randint(1, 100)
    number = rand_val * json_param
    operation = random.choice(OPERATIONS)
    return jsonify({"number": number, "operation": operation})


@app.route('/number/', methods=['DELETE'])
def delete_number():
    rand_val = random.randint(1, 100)
    operation = random.choice(OPERATIONS)
    return jsonify({"number": rand_val, "operation": operation})


# Раздел II. Отправка запросов на сервер с API. 
def run_client():
    url = "http://127.0.0.1:5000/number/"
    
    # GET
    param = random.randint(1, 10)
    r_get = requests.get(url, params={"param": param})
    data_get = r_get.json()
    print("GET", data_get)

    # POST
    json_param = random.randint(1, 10)
    r_post = requests.post(url, 
                           json={"jsonParam": json_param},
                           headers={"Content-Type": "application/json"})
    data_post = r_post.json()
    print("POST", data_post)

    # DELETE
    r_delete = requests.delete(url)
    data_delete = r_delete.json()
    print("DELETE", data_delete)

    # Составляем выражение и считаем
    n1, op1 = data_get["number"], data_get["operation"]
    n2, op2 = data_post["number"], data_post["operation"]
    n3, op3 = data_delete["number"], data_delete["operation"]

    print(f"\nСоставленное выражение: {n1} {op1} {n2} {op2} {n3}")

    result = float(n1)

    if op1 == "sum":
        result += n2
    elif op1 == "sub":
        result -= n2
    elif op1 == "mul":
        result *= n2
    elif op1 == "div":
        result = result / n2 if n2 != 0 else 0

    if op2 == "sum":
        result += n3
    elif op2 == "sub":
        result -= n3
    elif op2 == "mul":
        result *= n3
    elif op2 == "div":
        result = result / n3 if n3 != 0 else 0

    final = int(result)
    print(f"Результат = {final}\n")
    return final


print("1 — Запустить СЕРВЕР")
print("2 — Запустить КЛИЕНТ (Раздел II)")
choice = input("Выбери 1 или 2: ")

if choice == "1":
    print("\nСервер запущен на http://127.0.0.1:5000")
    print("Теперь открой НОВЫЙ терминал и запусти этот же файл → выбери 2")
    app.run(debug=False)
elif choice == "2":
    run_client()
else:
    print("Хз что хочешь")