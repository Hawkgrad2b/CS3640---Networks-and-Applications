# HW2 - Socket Programming
# Used 'https://www.geeksforgeeks.org/socket-programming-python/' to help with understanding
import socket
import sys
import os

HAWKID = 'wplucas'
NAME = 'William Lucas'

f = open('output.txt', 'w')

f.write(f'{HAWKID}\n{NAME}')

# Created a socket instance with the AF_NET as family IP4 address
# SOCK_STREAM is designates type as TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
f.write('Socket has been successfully created')
print('Socket has been successfully created')

host = sys.argv[0]
port = sys.argv[1]

s.bind((host, port))
f.write('Socket has been binded to port 5000 on the local host')
print('Socket has been binded to port 5000 on the local host')

s.listen()
f.write('socket is listening')
print('socket is listening')


print(f"server is running on {host}:{port}")
