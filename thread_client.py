import socket
import threading

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))  # Connect to the server

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Received from server: {message}")
        except:
            print("Disconnected from server.")
            client_socket.close()
            break

# Start receiving messages in a separate thread
threading.Thread(target=receive_messages, daemon=True).start()

# Send messages to the server
while True:
    message = input()
    client_socket.send(message.encode('utf-8'))
    if message.lower() == 'exit':
        client_socket.close() # formally closes the socket client-side
        break
    
