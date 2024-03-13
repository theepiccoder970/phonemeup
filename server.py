import socket
import threading
from contextlib import closing

def handle_client(conn, client_address):
    with conn:
        print(f"Connected by {client_address}")
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                # Echo back received data (for demonstration)
                conn.sendall(data)
            except ConnectionResetError:
                break

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def registration_server():
    host = '127.0.0.1'
    port = 12345  # Well-known port for registration
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Registration server listening on \{host\}:\{port\}")

        while True:
            conn, addr = server_socket.accept()
            chat_port = find_free_port()
            print(f"Assigning port {chat_port} to client {addr}")

            # Send the assigned chat port to the client\
            conn.send(str(chat_port).encode())

            # Start chat session on the new port\
            chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            chat_socket.bind((host, chat_port))
            chat_socket.listen(1)
            chat_conn, chat_addr = chat_socket.accept()

            client_thread = threading.Thread(target=handle_client, args=(chat_conn, chat_addr))
            client_thread.start()

if __name__ == "__main__":
    registration_server()
