# Socket Programming HW2

## Starting server.py:
1. In order to start this server, make sure you are 'cd' into the correct directory holding the file server.py
2. Open the terminal on what ever device you want to host the server on
3. run 'python3 server.py <PORT>'
4. <PORT> can be what ever port you want the server to link to, localhost is going to be the SERVER_IP by default
5. The server should start up and give the user multiple printouts letting them know it has started successfuly.
6. The terminal will display the SERRVER_IP and PORT that the user entered

## Starting client.py:
1. Repeat steps one and two to ensure correct set-up
2. Run 'python3 client.py <SERVER_IP> <PORT>'
3. <PORT> can be what ever port you want the server to link to
4. <SERVER_IP> should be 'localhost' since that is how server.py is set up
5. The client should start and give the user multiple printouts letting them know it is connecting and then connected 
6. The terminal will display the SERRVER_IP and PORT that the client is connected too

## Sending Messages:
- The client can type what ever they want to send to the other clients or sever
- Hit enter to send out the message you want to send

## Disconecting from the Server:
- Type '/quit' in the terminal and hit enter
- The client terminal should give the user multiple prinouts that it has succesfully disconnected

## CREDIT REEL:

### <h2> Source 1: 'https://www.cs.dartmouth.edu/~campbell/cs50/socketprogramming.html' </h2>
    - Build the foundational knowledge on how TCP sockets work and the overview on the structure of how establish the Client and Server sockets
    - Learned how each of the main functions, socket(), listen(), accept(), connect(), and bind() all worked.

### Source 2: 'https://sites.radford.edu/~hlee3/classes/itec350_spring2021/ClassNotes/Lecture9_SocketProgramming.pdf'
    - Explored the differencees of responsibilities between the client and server.
    - Examined what the difference between passive and active open, for both the server and client.
    - Leaned the flow of Orientation mode and Less mode of both the client and server.

### Source 3: 'https://www.geeksforgeeks.org/multithreading-python-set-1/'
    - This geeks for geeks page help build knowledge on previous materials from source 1 and 2.
    - Saw examples and visualizations of simple client and server scripts.
    - Introduced threading and how to use it's module 

### Source 4: 'https://www.geeksforgeeks.org/socket-programming-multi-threading-python/'
    - Analyzed a socket program that used multi-threading
    - Reference the structure on how to set up server and client programs.
