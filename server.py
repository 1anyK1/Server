import zmq
import json

BIND_ADDRESS = "tcp://*:5555"
OUTPUT_FILENAME = "locations.json"

def main():
    context = zmq.Context()
    
    socket = context.socket(zmq.PULL)
    
    try:
        socket.bind(BIND_ADDRESS)
        print("ZMQ PULL-сервер запущен и слушает на порту 5555...")
        print("Полученные данные будут записываться в файл locations.json")
    except zmq.error.ZMQError as e:
        print("Ошибка привязки сокета")
        return

    while True:
        try:
            message_bytes = socket.recv()
            message = message_bytes.decode('utf-8')
            try:
                with open(OUTPUT_FILENAME, 'a', encoding='utf-8') as f:
                    f.write(message + '\n') 
                print("Получены и сохранены новые GPS-данные)")
            except json.JSONDecodeError:
                print("Пришли неверные данные")
        except KeyboardInterrupt:
            print("\nСервер остановлен пользователем.")
            break
    socket.close()
    context.term()

if __name__ == "__main__":
    main()