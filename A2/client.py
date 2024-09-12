# client.py

import socket
import sys

server_address = (sys.argv[0], sys.argv[1]))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(server_address)

