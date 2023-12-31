from flask import Flask, request, render_template, send_from_directory
import socket
import json
from datetime import datetime
import threading

app = Flask(__name__)

# Функція для обробки статичних ресурсів (зображень)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)


# Функція для обробки головної сторінки
@app.route('/')
def index():
    return render_template('index.html')


# Функція для обробки сторінки з формою
@app.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        # Отримання даних з форми
        username = request.form['username']
        message_text = request.form['message']

        # Отримання поточного часу
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        try:
            with open("data.json", "r") as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = {}

        # Створення об'єкта з даними
        data = {
            'username': username,
            'message': message_text,
        }

        # Додавання нового запису до існуючих даних
        existing_data[current_time] = data

        with open("data.json", "w") as file:
            json.dump(existing_data, file, indent=4)

    return render_template('message.html')


# Функція для обробки помилки 404
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404


# Функція для відправки даних на Socket сервер
def send_to_socket_server(username, message_text):
    data = {
        'username': username,
        'message': message_text,
    }
    data_str = json.dumps(data)

    # Встановлення з'єднання з Socket сервером
    server_address = ('192.168.0.107', 5001)

    # Створення сокету
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(data_str.encode(), server_address)

# Функція для запуску Socket сервера
def run_socket_server():
    # Встановлюємо адресу та порт сервера
    server_address = ('192.168.0.107', 5001)

    # Створюємо UDP сокет
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        sock.bind(server_address)

        print("Socket сервер запущено на порту 5001")

        while True:
            # Очікуємо на дані
            data, _ = sock.recvfrom(1024)
            # Розкодовуємо отримані дані з байтів в рядок
            data_str = data.decode()
            # Перетворюємо рядок у словник
            data_dict = json.loads(data_str)
            # Обробляємо дані
            handle_data(data_dict)

if __name__ == '__main__':
    # Запуск Socket сервера в окремому потоці
    socket_server_thread = threading.Thread(target=run_socket_server)
    socket_server_thread.daemon = True
    socket_server_thread.start()

    # Запуск HTTP сервера на порту 5001
    app.run(port=5001, debug=True)

