# Krisham Prasai, hawkid=01411050
# client.py
# takes 2 arguments: server's ip and the port number
# does not show when other clients disconnect

import socket
import sys
import threading

# Function to write to the output file
def write_to_file(content):
    with open('output.txt', 'a') as f:
        f.write(content)

# Takes the client socket address and send a message to the server
def send_message(client_socket):
    while True:
        msg = input('Message: ')

        # Handles if a client wants to discconnect from the server
        if msg.lower() == '/quit':
            write_to_file('[CLIENT] A client is disconnecting from server...\n')

            try:
                msg = 'A client is disconnected from the server'
                client_socket.send(msg.encode('utf-8'))
                write_to_file('[CLIENT] A client has disconnected from the server\n')
                print('[CLIENT] A client has disconnected from the server\n')

            except socket.error as e:
                write_to_file('[CLIENT] Failed to send message. Error {e}\n')
                print('[CLIENT] Failed to send message. Error {e}\n')
                break

            # Closes the socket after client wants to quit
            client_socket.close()            
            break
        
        # If message is not '/quit' send the desired client message to the server
        try:
            client_socket.send(msg.encode('utf-8'))
        except socket.error as e:
            write_to_file('[CLIENT] Failed to send message. Error {e}\n')
            print('[CLIENT] Failed to send message. Error {e}\n')
            break

# Handles the server's broadcasts and other client messages sent to this client
def recieve_message(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)

            # If no data is recieved, server must be closed
            if not data:
                write_to_file('[CLIENT] Connection closed by server\n')
                print('[CLIENT] Connection closed by server\n')
                break
            
            # Decodes the message sent by server or other clients
            decoded_msg = data.decode('utf-8')
            write_to_file(f'Server: {decoded_msg}\n')
            print(f'Server: {decoded_msg}\n')

        # Handles socket errors when revieving messages
        except socket.error:
            write_to_file('[CLIENT] Error recieving message from server\n')
            print('[CLIENT] Error recieving message from server\n')
            break

# Created a client socket instance with the AF_NET as family IP4 address,
# SOCK_STREAM designates type as TCP. Takes arguments from the terminal as
# the SERVER_IP and PORT to be used
def start_client():

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Takes the system arguments as SERVER_IP AND PORT
    SERVER_IP = sys.argv[1]
    PORT = int(sys.argv[2])

    write_to_file(f'[CLIENT] Connecting to {SERVER_IP} on port {PORT}\n')
    print(f'[CLIENT] Connecting to {SERVER_IP} on port {PORT}\n')

    # Connect to the servber if possible
    try:
        client_socket.connect((SERVER_IP, PORT))
        write_to_file(f'[CLIENT] Connected to {SERVER_IP} on port {PORT}\n')
        print(f'[CLIENT] Connected to {SERVER_IP} on port {PORT}\n')

    # Handles the errors when trying to connect to the server
    except socket.error as e:
        write_to_file(f'[CLIENT] Connection to server failed. Error: {e}')
        print(f'[CLIENT] Connection to server failed. Error: {e}')
        client_socket.close()
        sys.exit(1)

    # Create the threads for sending and recieving, with the current client socket
    send_thread = threading.Thread(target= send_message, args= (client_socket,))
    recieve_thread = threading.Thread(target= recieve_message, args=(client_socket,))

    # Start the threads
    send_thread.start()
    recieve_thread.start()

    # Holds program until the thread is has completed
    send_thread.join()
    recieve_thread.join()

    write_to_file('[CLIENT] Client connection closed\n')
    print('[CLIENT] Client connection closed\n')

# Starts the client, only if it has correct number of arguments passed in
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('[ERROR] Please format: python3 clienty.py <SERVER_IP> <PORT>\n')
        sys.exit(1)
    start_client()
