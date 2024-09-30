**A2**:
includes server.py, client.py, and output.txt; 
usage for server.py: python3 server.py (serverip) (port) eg local host 8080; 
usage for client.py: python3 client.py (port) eg 8080

Creates a TCP socket connection between server and clients. Can handle multiple clients. Clients send messages that are received by server and other clients. To exit a client program type '/quit'. To exit the server you must manually exit in terminal eg ^C. The programs also log important data to output.txt as the progrms are running.

Credits: Used chatGPT to help with threading implementation. Also used it as a study tool to understand both modules (socket, threading). It worked best as a general understanding tool. I found that often trying to prompt it was more difficult than thinking about the problem myself.