import socket
import threading
import datetime

class new_Client:
    def __init__(self, client_num, socket, open_time, close_time):
        self.client_num = client_num
        self.client_socket = socket
        self.open_time = open_time 
        self.close_time = close_time

    def set_close_time(self,close_time):
        self._close_time = close_time

index = 1

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))  # Bind to localhost on port 12345
server_socket.listen(5)  # Allow up to 5 queued connections
#.listen enables server to accept connections (# = clients)
print("Server is listening...")

clients = []

def handle_client(client_socket, address):
    global index 
    client = new_Client(index, client_socket,datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),0)
    index += 1
    clients.append(client)

    print(f"Client: {client.client_num}, Socket: {client.client_socket}, Opened at: {client.open_time}")


    #index= clients.index(client_socket)

    print(f"New connection from {address}; Client {client.client_num}")

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            
            #"Recieved from {addresss}"
            print(f"Received from Client {client.client_num}: {message}")
            broadcast(message, client_socket)

        except:
            break
    
    print(f"Connection closed: {address}")
    client.set_close_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    clients.remove(client)
    client_socket.close()

def broadcast(message, sender_socket):
    for client in clients:

        if client.client_socket == sender_socket:
            client.client_socket.send((message + " ACK").encode())

            if message.lower() == 'status':
                print("Listings:")

        elif client.client_socket != sender_socket:
            try:
                client.client_socket.send(message.encode())
            except:
                client.close_time()
                clients.remove(client)
                print(f"After Removing: {clients}")

while True:
    client_socket, addr = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_thread.start()

def print_cache(clients):
    for client in clients:
        print(client.index)
        print(client.index)
        print(client.index)
        print(client.index)

    print("Hello World")