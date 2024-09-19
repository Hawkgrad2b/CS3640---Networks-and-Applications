# Krisham Prasai, hawkid=01411050
# client.py
# takes 2 arguments: server's ip and the port number
# does not show when other clients disconnect

import socket
import sys
import threading

log_file = 'output.txt'
# since messages and connection status are logged by server, 
# we only need to log errors on the client side
def log_error(error):
    print(error)
    with open(log_file,'a') as file:
        file.write('\n' + error + '\n')

client_running = True
def receive_messages(client_socket):
    global client_running
    while client_running:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"\nReceived from server: {message}\n"
                    "Enter message to send ('/quit' to exit): ",end='')
        except Exception as e:
            if client_running:
                log_error(f"Error in receiving messages: {e}")
                break

def start_client(server_ip, port):
    global client_running
    try:
        client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client_socket.connect((server_ip, port))
        print("Connected to server.\n")
        
        receive_thread = threading.Thread(target=receive_messages,
                                          args=(client_socket,))
        
        # Ensure thread exits when main program exits
        receive_thread.daemon = True
        
        receive_thread.start()

        while True:
            message = input("Enter message to send ('/quit' to exit): ")
            if message.lower() == '/quit':
                break
            client_socket.send(message.encode('utf-8'))
    except Exception as e:
        log_error(f"Error: {e}")
    finally:
        # this is reached if client quit
        print("Disconnecting...")
        client_socket.close()
        sys.exit(0)

if __name__=="__main__":
    # check for correct arguments
    if len(sys.argv) != 3:
        print("Please input two parameters, the server IP and the port.")
        sys.exit()
    
    # this will log errors for incorrect argument type
    try:
        server_ip = sys.argv[1]
        port = int(sys.argv[2])
    except Exception as e:
        log_error(f"Error: {e}")
        sys.exit()
        
    start_client(server_ip, port)

       
