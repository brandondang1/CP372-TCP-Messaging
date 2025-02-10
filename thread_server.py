import socket
import threading
import datetime
import os 

class new_Client:
    def __init__(self, client_num, socket, open_time):
        self.client_num = client_num
        self.client_socket = socket
        self.open_time = open_time 
        self.close_time = None

    def set_close_time(self,close_time):
        self._close_time = close_time

def print_cache():
    message = ""
    for client in clients:
        message += f"Client: {client.client_num}, Socket: {client.client_socket}, Opened at: {client.open_time}, Closed at: {client.close_time}\n"
        print(message)
        return message


index = 1
files_dir = "server_files"  # Directory where files are stored
if not os.path.exists(files_dir):
    os.makedirs(files_dir)

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))  # Bind to localhost on port 12345
server_socket.listen(5)  # Allow up to 5 queued connections
#.listen enables server to accept connections (# = clients)
print("Server is listening...")

clients = []

def handle_client(client_socket, address):
    global index 
    client = new_Client(index, client_socket, datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
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
            if message.lower() == 'status':
                message = ""
                for client in clients:
                    listing = print_cache()
                    client.client_socket.send(listing.encode('utf-8'))
            elif message.lower() == "list":
                file_list = os.listdir(files_dir)
                client.client_socket.send("\n".join(file_list).encode('utf-8'))
            elif message.startswith("get "):
                filename = message.split(" ")[1]
                filepath = os.path.join(files_dir, filename)
                if os.path.exists(filepath):
                    with open(filepath, "rb") as file:
                        client.client_socket.send(file.read())
                else:
                    client_socket.send(f"File '{filename}' not found".encode('utf-8'))
            else:
                client.client_socket.send((message + " ACK").encode())


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