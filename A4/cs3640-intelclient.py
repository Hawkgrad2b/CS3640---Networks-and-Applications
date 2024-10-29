# not sure if this works yet

import socket
import sys

def main():
    if len(sys.argv) != 5:
        print("Usage: python3 cs3640-intelclient.py <server_addr> <server_port> <domain> <service>")
        sys.exit(1)

    server_addr = sys.argv[1]
    server_port = int(sys.argv[2])
    domain = sys.argv[3]
    service = sys.argv[4]

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((server_addr, server_port))
            command = f"{service}({domain})"
            sock.sendall(command.encode('utf-8'))
            response = sock.recv(4096).decode('utf-8')
            print(response)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
