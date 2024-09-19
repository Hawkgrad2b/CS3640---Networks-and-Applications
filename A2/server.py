# Krisham Prasai, hawkid=01411050
# server.py
# takes one argument, the port number
# logs conversation in output.txt
# manually ^C to exit the program

import socket
import sys
import threading

# log communication in output.txt
log_file = 'output.txt'

def log_message(message):
    print(message)
    with open(log_file, 'a') as file:
        file.write(message)

# keep track of connected clients
clients = []

def handle_client(client_socket, client_address):
        try:
            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                
                log_message(f"\nRecieved from {client_address}: {message}")

                # broadcast to all clients except sender
                broadcast_message(message, client_socket)
        
        except Exception as e:
            log_message(f"\nError: {e}")
        
        finally:
            log_message(f"\nClient {client_address} disconnected")
            client_socket.close()
            clients.remove(client_socket)

def broadcast_message(message, sender_socket):
    for client in clients:
        if client != sender_socket: # don't send back to sender
            try:
                client.send(f"\n{message}".encode('utf-8'))
            
            except Exception as e:
                log_message(f"Error sending message to client: {e}")
                client.close()
                clients.remove(client)

def start_server(port):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.listen(1000)
        log_message(f"Server listening on port {port}")
        
        while True:
            client_socket, client_address = server_socket.accept()
            log_message(f"\nNew connection from {client_address}")
            clients.append(client_socket)
            client_thread = threading.Thread(target=handle_client,
                                             args=(client_socket,
                                                   client_address))
            client_thread.start()
    
    except Exception as e:
        log_message(f"Error: {e}")
    
    finally:
        server_socket.close()

if __name__ == "__main__":

    # check for correct arguments
    if len(sys.argv) != 2:
        log_message("Use port number as a single argument.")
        sys.exit()

    # clear output file whenever we call server.py again
    with open(log_file, 'w') as file:
        file.write('Krisham Prasai 01411050\n')
    
    port = int(sys.argv[1])
    start_server(port)


