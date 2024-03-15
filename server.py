# Import Modules
import socket
import threading
import tkinter as tk


HOST = '127.0.0.1'
PORT = 1234
LISTENER_LIMIT = 5
active_clients = [] # List of all currently connected users

# Function to listen for upcoming messages from client
def listen_for_messages(client, username):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            final_msg = f'{username} ~ {message}'
            send_messages_to_all(final_msg)
        else:
            print(f'The message send from client {username} is empty')

# Message to a single client
def send_message_to_client(client, message):
    client.sendall(message.encode())

# Function to send any new message to all the clients
def send_messages_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1], message)

# Function to handle client
def client_handler(client):
    # Server will listen message ( contain username )
    while 1:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            prompt_message = f'SERVER~ {username} added to the chat'
            send_messages_to_all(prompt_message)
            break
        else:
            print('Client username is empty')
    threading.Thread(target=listen_for_messages, args=(client, username)).start()

def main():
    # AF_INET use ipv4
    # SOCK_STREAM use tcp packets for communication
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        server.bind((HOST,PORT))
        print(f'[Running the server on {HOST} {PORT}]')
    except:
        print(F'Unable to bin to host {HOST} and port {PORT}')
    
    server.listen(LISTENER_LIMIT)
    
    # Listening to client connections
    while 1:   
        client, address = server.accept()
        print(f'Successfully connected to client {address[0]} {address[1]}')
        
        threading.Thread(target=client_handler, args=(client, )).start()

if __name__ == '__main__':
    main()