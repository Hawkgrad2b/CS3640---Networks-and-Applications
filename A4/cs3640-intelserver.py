# Server to provide network intelligence services to clients
# Listens on 127.0.0.1 via port 5555
import socket
import dnspython
import ssl

def get_IPV4_ADDR(domain):
    return

def get_IPV6_ADDR(domain):
    return

def get_TLS_CERT(domain):
    return 

def get_HOSTING_AS(domain):
    return

def get_ORGANIZATION(domain):
    return


def start_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('127.0.0.1', 5555))
    server_sock.listen(5)
    print('Server has been started and is listening on port 5555...')

    while True:
        client_socket, addr = server_sock.accept()
        print(f'Connection from {addr} has been established')

        data = client_socket.recv(1024).decode('utf-8')
        print(f'Recieved command: {data}')
        
        try:
            command, domain = data.strip().split("(", 1)
            domain = domain[:-1]
            command  command.strip()
            domain = domain.strip()
        except ValueEorror: 
            response = "ERROR: Invalid command format."
            client_socket.send(response.encode('utf-8'))
            client_socket.close()
            continue

        if command == "IPV4_ADDR":
            response = get_IPV4_ADDR(domain)
        elif command == "IPV6_ADDR":
            response = get_IPV6_ADDR(domain)
        elif command == "TLS_CERT":
            response = get_TLS_CERT(domain)
        elif command == "HOSTING_AS":
            response = get_HOSTING_AS(domain)
        elif command == "ORGANIZATION":
            response = get_ORGANIZATION(domain)
        else:
            response = "Unknown command."
        
        client_socket.send(response.encode('utf-8'))
        client_socket.close()

if __name__ == "__main__":
    start_server()
