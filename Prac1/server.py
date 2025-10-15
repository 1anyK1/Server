import socket

PORT = 8080
BUFFER_SIZE = 1024

def main():
    server_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_fd.bind(("0.0.0.0", PORT))

    server_fd.listen(3)
    print(f"[*] Сервер слушает на порту {PORT}...")

    conn, addr = server_fd.accept()
    print(f"[+] Подключение от {addr}")

    data = conn.recv(BUFFER_SIZE).decode("utf-8")
    print(f"Получено: {data}")

    hello = "Hello from server"
    conn.sendall(hello.encode("utf-8"))
    print("Сообщение отправлено")

    conn.close()
    server_fd.close()

if __name__ == "__main__":
    main()
