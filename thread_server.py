"""
------------------------------------------------------------------------
CP372 Programming Assignment
------------------------------------------------------------------------
Authors: Brandon Dang, Daniel Gao
IDs: 169026034, 169041875
Emails: dang6034@mylaurier.ca, gaox1875@mylaurier.ca
Last edited: "2025-02-10"
------------------------------------------------------------------------
"""
import socket
import threading
import datetime
import os 

class new_Client: # Client object
    def __init__(self, client_num, socket, open_time):
        self.client_num = client_num
        self.client_socket = socket
        self.open_time = open_time 
        self.close_time = None
        self.name = None

    def set_close_time(self, closed):
        self.close_time = closed

    def set_name(self, username):
        self.name = username

def print_cache():
    message = ""
    for client in clients:
        message += f"Client: {client.client_num}, Name: {client.name}, Socket: {client.client_socket}, Opened at: {client.open_time}, Closed at: {client.close_time}\n"
    print(message)
    return message

MAX_CLIENTS = 3
active_clients = 0
index = 1
files_dir = "server_files"  # Directory where files are stored
if not os.path.exists(files_dir):
    os.makedirs(files_dir)

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))  # Bind to localhost on port 12345
server_socket.listen(MAX_CLIENTS + 1) # Allows up to MAX_CLIENTS + 1
#.listen enables server to accept connections (# = clients)
print("Server is listening...")

clients = []

def handle_client(client_socket, address):
    global index, active_clients
    message_count = 0
    client = new_Client(index, client_socket, datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
    index += 1
    clients.append(client)
    active = True 
    print(f"Client: {client.client_num}, Socket: {client.client_socket}, Opened at: {client.open_time}")


    #index= clients.index(client_socket)

    print(f"New connection from {address}; Client {client.client_num}")
    client_socket.send("Please enter a name: ".encode('utf-8'))
    
    while active:
        message = client_socket.recv(1024).decode('utf-8') # recieves messages from the client
        if not message:
            break
        
        #"Recieved from {addresss}"
        print(f"Received from Client {client.client_num}: {message}")
        if message_count > 0:
            active = broadcast(message, client_socket, client.name)
        else:
            client.set_name(message)
            client_socket.send(f"Your name is set as: {client.name}".encode('utf-8'))
        message_count += 1
    
    print(f"Connection closed: {address}")
    client.set_close_time(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
    #clients.remove(client)
    client_socket.close()
    active_clients -= 1

def broadcast(message, sender_socket, sender_name):
    for client in clients:
        if client.close_time is not None:
            pass
        elif client.client_socket == sender_socket:
            if message.lower() == 'status':
                listing = print_cache()
                client.client_socket.send(listing.encode('utf-8'))
            elif message.lower() == "list": # gets the list of files in the repo
                file_list = os.listdir(files_dir)
                client.client_socket.send("\n".join(file_list).encode('utf-8'))
            elif message.startswith("get "): # returns the file contents of requested file
                filename = message.split(" ")[1]
                filepath = os.path.join(files_dir, filename)
                if os.path.exists(filepath): # checks if the file exists
                    with open(filepath, "rb") as file:
                        client.client_socket.send(file.read())
                else: 
                    client_socket.send(f"File '{filename}' not found".encode('utf-8'))
            elif message.lower() == 'exit':
                return False
            else:
                client.client_socket.send((message + " ACK").encode('utf-8'))
        elif client.client_socket != sender_socket and client.close_time is None:
            client.client_socket.send(f"{sender_name}: {(message)}".encode('utf-8'))
    return True


while True:
    client_socket, addr = server_socket.accept()
    if active_clients < MAX_CLIENTS: # checking if there are more than the allowed limit of clients connected
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()
        active_clients += 1
    else:
        client_socket.send("Server is full, try again later.".encode('utf-8'))
        client_socket.close()
