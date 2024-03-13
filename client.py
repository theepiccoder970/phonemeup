import socket

def start_client(server_host='127.0.0.1', registration_port=12345):
    # Connect to server's registration port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((server_host, registration_port))
        assigned_port = int(sock.recv(1024).decode())
        print(f"Assigned chat port: {assigned_port}")

    # Connect to the assigned chat port\
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as chat_sock:
        chat_sock.connect((server_host, assigned_port))
        print("Connected to chat. Type 'exit' to quit.")
        while True:
            message = input("Message: ")
            if message.lower() == 'exit':
                break
            chat_sock.sendall(message.encode())
            data = chat_sock.recv(1024)
            print(f"Received: {data.decode()}")

if __name__ == "__main__":
    start_client()\

