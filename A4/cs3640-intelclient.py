# cs3640-intelclient.py

import socket
import sys
import logging

logging.basicConfig(
    filename='cs3640-intelClient.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    if len(sys.argv) != 5:
        logging.error("Incorrect number of arguments.")
        print("Usage: python3 cs3640-intelclient.py <server_addr> <server_port> <domain> <service>")
        sys.exit(1)
    
    # Assign command-line arguments to variables
    server_addr = sys.argv[1]
    server_port = int(sys.argv[2])
    domain = sys.argv[3]
    service = sys.argv[4]

    try:
        # Create a TCP socket and connect to server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            logging.info(f"Connecting to server at {server_addr}:{server_port}...")
            print(f"Connecting to server at {server_addr}:{server_port}...")
            sock.connect((server_addr, server_port))
            
            # Format the command according to server requirements
            command = f"{service}({domain})"
            logging.info(f"Sending command: {command}")
            print(f"Sending command: {command}")

            # Send command to server
            sock.sendall(command.encode('utf-8'))

            # Receive the response from the server
            response = sock.recv(8192).decode('utf-8')
            logging.info(f"Received response: {response}")
            print("Response from server: ", response)
    
    except Exception as e:
        logging.error(f"Error: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

