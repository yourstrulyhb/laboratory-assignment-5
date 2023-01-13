# Laboratory Exercise 5
# Hannah Bella Arceño
# Karmela Castro
# BS Computer Science IV

import socket
from threading import Thread
import sys 

# server's IP address
SERVER_HOST = "127.0.0.1" #"0.0.0.0"
SERVER_PORT = 1234 # port we want to use
separator_token = "<SEP>" # we will use this to separate the client name & message

print("Hi! I'm Eve. I'm the channel for exchanging keys!\n")

client_sockets = set() # list/set of all connected client's sockets

# create a TCP socket
s = socket.socket()

# make the port as reusable port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind the socket to the address we specified
s.bind((SERVER_HOST, SERVER_PORT))

# listen for upcoming connections
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

def listen_for_client(cs):
    """
    This function keep listening for a message from `cs` socket
    Whenever a message is received, broadcast it to all other connected clients
    """
    while True:
        try:
            # keep listening for message from `cs` socket
            msg = cs.recv(1024).decode()

        except Exception as e:
            # If client no longer connected
            # remove it from the set
            print(f"[!] Error: {e}") 
            client_sockets.remove(cs)

            if (len(client_sockets) == 0):
                return 
            
        else:
            # if we received a message, replace <SEP> 
            # with ": " when printing
            msg = msg.replace(separator_token, ": ")

        # send message to connected clients
        for client_socket in client_sockets:
            client_socket.send(msg.encode())


while True:
    # we keep listening for new connections all the time
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
   
    client_sockets.add(client_socket)    # add the new connected client to connected sockets
    
    # start a new thread that listens for each client messages
    t = Thread(target=listen_for_client, args=(client_socket,))
    
    t.daemon = True # make the thread daemon so it ends whenever the main thread ends
    
    t.start() # start thread

# close client sockets
for cs in client_sockets:
    cs.close()

# close server socket
s.close()
