import zmq
import json
import psycopg2

BIND_ADDRESS = "tcp://*:5555"
OUTPUT_FILENAME = "locations.json"

def main():
    conn = psycopg2.connect(dbname = "db_server", host= "localhost", user="postgres", password="postgres1234", port="5432")

    print("Database connected")

    curs = conn.cursor()

    context = zmq.Context()
    
    socket = context.socket(zmq.PULL)
    
    try:
        socket.bind(BIND_ADDRESS)
        print("ZMQ PULL-сервер запущен и слушает на порту 5555...")
    except zmq.error.ZMQError as e:
        print("Ошибка привязки сокета")
        return

    while True:
        try:
            message_bytes = socket.recv()
            data = json.loads(message_bytes)
            lat = data['latitude']
            lon = data['longitude']
            rsrp = data['RSRP']
            rsrq = data['RSRQ']
            rssi = data['RSSI']
            timest = data['timestamp']

            curs.execute("INSERT INTO info_abonent (lat, lon, rsrp, rsrq, rssi, timestamp) " \
            "values (%s, %s, %s, %s, %s, %s)", (lat, lon, rsrp, rsrq, rssi, timest))
            conn.commit()

            print("Server recv data")

        except KeyboardInterrupt:
            print("\nСервер остановлен пользователем.")
            break
    socket.close()
    context.term()
    curs.close()
    conn.close()

if __name__ == "__main__":
    main()