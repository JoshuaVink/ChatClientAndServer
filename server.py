import socket

HOST = '127.0.0.1'  # Localhost
PORT = 5000         # Same port as client

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()
    print("Server is running... Waiting for connections.")
    
    conn, addr = server.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            message = input("Enter message to send: ")
            conn.sendall(message.encode())
