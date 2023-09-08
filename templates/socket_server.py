import socket
import json

# Функція для обробки даних і зберігання їх у файлі
def handle_data(data):
    with open('storage/data.json', 'a') as file:
        timestamp = data.get('timestamp', str(datetime.now()))
        file.write(f'"{timestamp}": {json.dumps(data)},\n')

# Функція для запуску Socket сервера
def run_socket_server():
    # Встановлюємо адресу та порт сервера
    server_address = ('192.168.0.107', 5000)

    # Створюємо UDP сокет
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(server_address)

        print("Socket сервер запущено на порту 5000")

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
    run_socket_server()  # Запускаємо Socket сервер
