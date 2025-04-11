import socket
from threading import Thread

HOST = '127.0.0.1'
PORT = 5003
clients = []  # List to keep track of connected clients


# Function to handle a single client
def handleClient(sock, addr):
    print(f"Client connected: {addr}")
    clients.append(sock)

    try:
        while True:
            data = sock.recv(1024)
            if not data:
                break  # Client disconnected
            print(f"Message from {addr}: {data.decode()}")
            sendToAll(data, sock)
    except Exception as e:
        print(f"Error with {addr}: {e}")
    finally:
        print(f"Client {addr} disconnected.")
        if sock in clients:
            clients.remove(sock)
        sock.close()


def sendToAll(message, sender_socket):
    for client in clients[:]:  # Copy to avoid issues during removal
        try:
            client.sendall(message)
        except:
            clients.remove(client)
            client.close()


# Main server setup
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print("Server is running... Waiting for connections.")

    try:
        while True:
            connection_socket, addr = server_socket.accept()
            t = Thread(target=handleClient, args=(connection_socket, addr))
            t.start()
    except KeyboardInterrupt:
        print("\nServer shutting down.")
        server_socket.close()
