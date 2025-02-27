# Server to provide network intelligence services to clients
# Listens on 127.0.0.1 via port 5555
import socket
import json
import dns.resolver
import ssl
from ipwhois import IPWhois
import logging
import sys
import signal

logging.basicConfig(
    filename='cs3640-intelServer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_IPV4_ADDR(domain):
    try:
        result = dns.resolver.resolve(domain, 'A')
        return str(result[0])
    except Exception as e:
        logging.error(f'Error resolving IPv4 address for {domain}: {str(e)}')
        return f'Error resolving IPv4 address: {str(e)}'

def get_IPV6_ADDR(domain):
    try:
        result = dns.resolver.resolve(domain, 'AAAA')
        return str(result[0])
    except Exception as e:
        logging.error(f'Error resolving IPv6 address for {domain}: {str(e)}')
        return f'Error resolving IPv6 address: {str(e)}'

def get_TLS_CERT(domain):
    try:
        port = 443
        context = ssl.create_default_context()
        with socket.create_connection((domain, port)) as sock:
            with context.wrap_socket(sock, server_hostname= domain) as ssock:
                cert = ssock.getpeercert()
                return cert # return as a dictionary
    except Exception as e:
        logging.error(f"Error retrieving TLS certificate for {domain}: {str(e)}")
        return f"Error retrieving TLS certificate: {str(e)}"

def get_HOSTING_AS(domain):
    try:
        ip_addr = get_IPV4_ADDR(domain)
        if 'Error' in ip_addr:
            return ip_addr  # Return the error message
        # WHOIS
        obj = IPWhois(ip_addr)
        results = obj.lookup_whois()
        asn = results.get('asn')
        asn_description = results.get('asn_description')
        if asn and asn_description:
            return f'AS{asn} - {asn_description}'
        else:
            return "Hosting AS information not found."
    except Exception as e:
        logging.error(f"Error retrieving hosting AS for {domain}: {str(e)}")
        return f"Error retrieving hosting AS: {str(e)}"

def get_ORGANIZATION(domain):
    try:
        cert = get_TLS_CERT(domain)
        if isinstance(cert, str) and 'Error' in cert:
            return cert  # Return the error message from get_TLS_CERT
        
        subject = cert.get('subject', [])
        organization = None
        for item in subject:
            # Each item is a list of tuples
            for attribute in item:
                key = attribute[0]
                value = attribute[1]
                if key == 'organizationName' or key == 'O':
                    organization = value
                    return organization  
        
        # If organization not found after looping
        return "Organization not found in TLS certificate."
    except Exception as e:
        logging.error(f"Error retrieving organization for {domain}: {str(e)}")
        return f"Error retrieving organization: {str(e)}"


def start_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('127.0.0.1', 5555))
    server_sock.listen(5)
    logging.info("Server started and listening on port 5555.")
    print('Server has been started and is listening on port 5555...')

    def shutdown_server(signum, frame):
        # graceful shutdown for the sever
        logging.info("Shutting down the server...")
        print("Shutting down the server...")
        server_sock.close()
        sys.exit(0)

    # register the signal for shutdown 'CTRL C'
    signal.signal(signal.SIGINT, shutdown_server)

    try:
        while True:
            client_socket, addr = server_sock.accept()
            logging.info(f'Connection from {addr} established.')
            print(f'Connection from {addr} has been established')
        

            data = client_socket.recv(1024).decode('utf-8')
            logging.info(f'Received command: {data}')
            print(f'Recieved command: {data}')
            
            try:
                command, domain = data.strip().split("(", 1)
                domain = domain[:-1]
                command = command.strip()
                domain = domain.strip()
            except ValueError: 
                response = "ERROR: Invalid command format."
                client_socket.send(response.encode('utf-8'))
                client_socket.close()
                logging.error("Invalid command format received.")
                continue

            if command == "IPV4_ADDR":
                response = get_IPV4_ADDR(domain)
            elif command == "IPV6_ADDR":
                response = get_IPV6_ADDR(domain)
            elif command == "TLS_CERT":
                cert = get_TLS_CERT(domain)
                response = json.dumps(cert) if isinstance(cert, dict) else cert
            elif command == "HOSTING_AS":
                response = get_HOSTING_AS(domain)
            elif command == "ORGANIZATION":
                response = get_ORGANIZATION(domain)
            else:
                response = "Unknown command."
                logging.warning(f"Unknown command received: {command}")

            client_socket.send(response.encode('utf-8'))
            logging.info(f'Sent response: {response}')
            client_socket.close()

    except KeyboardInterrupt:
        shutdown_server(None, None)

if __name__ == "__main__":
    start_server()

