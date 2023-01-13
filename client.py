# Laboratory Exercise 5
# Hannah Bella Arceño
# Karmela Castro
# BS Computer Science IV

import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back
import sys

# initialize colors
init()

# set the available colors
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
]

# choose a random color for the client
client_color = random.choice(colors)

# server's IP address
# if the server is not on this machine, 
# put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 1234 # server's port
separator_token = "<SEP>" # we will use this to separate the client name & message

# initialize TCP socket
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

# display the commands to the client
# the commands will help the user solve for their public and secret key
print("""
    Commands:
        sendmypublickey - compute public key and send to other client.
        getsecretkey    - get public key of other client and compute secret key.
        quit             - exit
    """)

# ask the client for a name
name = input("Enter your name: ")
# ask the client for a private key
priv_key = int(input("Enter your private key: "))

def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        print("\n" + message)

# make a thread that listens for messages to this client & print them
t = Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()

# define the P and G values
P = 11
G = 7

# get the public key of the client and send it
def get_key(priv_key):
    return int(pow(G,priv_key,P))

# get the private key of the client and send it
def get_secret(priv_key, x):
    return int((x**priv_key)%P)

while True:
    # input message we want to send to the server
    to_send =  input("Enter command: ")
    # a way to exit the program
    if to_send.lower() == 'quit':
        break
        
    # solve and send the public key to other client
    elif to_send.lower() == 'sendmypublickey':
        to_send = get_key(priv_key)

    # solve and send your private key
    elif to_send.lower() == 'getsecretkey':
        # ask the user for their public key
        x = int(input("Enter public key of other: "))
        
        # solve and get secret key
        secret_key = get_secret(priv_key, x)
        
        # display the secret key to client
        print("Secret key: ", secret_key)

        sys.exit() # quit program since secret key computed

    # add the datetime, name & the color of the sender
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    to_send = f"{client_color}[{date_now}] {name}{separator_token}{to_send}{Fore.RESET}"
    # finally, send the message
    s.send(to_send.encode())

# close the socket
s.close()
