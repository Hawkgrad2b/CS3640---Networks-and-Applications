# HW2 - Socket Programming
# Used 'https://www.geeksforgeeks.org/socket-programming-python/' to help with understanding
import socket
import sys
import threading

HAWKID = 'wplucas'
NAME = 'William Lucas'

def write_to_file(content):
    with open('output.txt', 'a') as f:
        f.write(content)

# Holds the client_socket address for all clients who connect to the server
CLIENTS = []

# Handles the logic when a client tries to connect, and when a message is sent
def handle_clients(client_socket, client_addr):
    write_to_file(f'[SERVER] New thread from {client_addr}\n')
    print(f'[SERVER] New thread from {client_addr}\n')
    CLIENTS.append(client_socket)

    try:
        while True:
            try:   
                data = client_socket.recv(1024)

                # If no data is recieved, client must be disconnected
                if not data:
                    write_to_file(f'[SERVER] Client {client_addr} disconnected\n')
                    print(f'[SERVER] Client {client_addr} disconnected\n')
                    break
                
                # Decodes the message sent by client and sends to all others
                decoded_msg = data.decode('utf-8')
                write_to_file(f'[SERVER] Recieved from {client_addr}: {decoded_msg}\n')
                print(f'[SERVER] Recieved from {client_addr}: {decoded_msg}\n')

                # Sends out the message that a client has sent it,
                # a broadcast to all other clients 
                send_broadcast_msg(f'{client_addr} says: {decoded_msg}', client_socket)

            # Handles socket errors with clients
            except socket.error:
                write_to_file(f'Error with connection {client_addr}')
                print(f'Error with connection {client_addr}')
                break

    finally:
        # Remove the client from active connections and close the connection
        if client_socket in CLIENTS:
            CLIENTS.remove(client_socket)

        client_socket.close()
        write_to_file(f'[SERVER] Connection with {client_addr} is closed\n')
        print(f'[SERVER] Connection with {client_addr} is closed\n')

# Sends out the broadcast message from one client to all other clients
def send_broadcast_msg(msg, sender_socket):
    for client in CLIENTS:
        # already checked for no data inside 'handle_clients' 
        # method before passing in msg
        if client != sender_socket:
            encoded_msg = msg.encode('utf-8')
            client.send(encoded_msg)

# Created a server socket instance with the AF_NET as family IP4 address,
# SOCK_STREAM designates type as TCP
def start_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    write_to_file('[SERVER] Socket has been successfully created\n')
    print('[SERVER] Socket has been successfully created\n')

    HOST = 'localhost'
    PORT = int(sys.argv[1])

    # Binds the socket to the local host and the specified port
    server_socket.bind((HOST, PORT))
    write_to_file(f'[SERVER] Server is starting on {HOST} from port {PORT}\n')
    print(f'[SERVER] Server is starting on {HOST} from port {PORT}\n')

    # Listens for client connections
    server_socket.listen(5)
    write_to_file('[SERVER] Server is listening...\n')
    print('[SERVER] Server is listening...\n')

    try:
        while True:
            # also the 'conn' variable
            client_socket, client_addr = server_socket.accept()
            write_to_file(f'[SERVER] New connection established with {client_addr}\n')
            print(f'[SERVER] New connection established with {client_addr}\n')

            # Creates the client thread for the current connection 
            client_thread = threading.Thread(target= handle_clients, args= (client_socket, client_addr))

            #Starts the thread connection with the client
            client_thread.start()
            write_to_file(f'[SERVER] Started thread with {client_addr}\n')
            print(f'[SERVER] Started thread with {client_addr}\n')

    finally:
        server_socket.close()
        write_to_file(f'[SERVER] Connection with {client_addr} has been closed\n')
        print(f'[SERVER] Connection with {client_addr} has been closed\n')

# Resets the output file each time the server is started
with open('output.txt', 'w') as f:
    f.write(f'{HAWKID}\n{NAME}\n')

# Starts the server, only if it has correct number of arguments passed in 
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('[ERROR] Please format: python3 server.py <PORT>\n')
        sys.exit(1)
    start_server()
