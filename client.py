import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back
import sys

# init colors
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

print("""
    Commands:
        sendmypublickey - compute public key and send to other client.
        getsecretkey    - get public key of other client and compute secret key.
        quit             - exit
    """)
# prompt the client for a name
name = input("Enter your name: ")
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

P = 11
G = 7
#Alice_priv_key = 3
#Bob_priv_key = 5

#def get_key(name):
def get_key(priv_key):
    return int(pow(G,priv_key,P))
    #if name.lower() == "alice":
        #alice_pub = int(pow(G,Alice_priv_key,P))
        #return alice_pub
    #elif name.lower() == "bob":
        #bob_pub = int(pow(G,Bob_priv_key,P))
        #return bob_pub

def get_secret(priv_key, x):
    return int((x**priv_key)%P)
    #if name.lower() == "alice":
        #alice_ka = int((x**Alice_priv_key)%P)
        #return alice_ka
    #elif name.lower() == "bob":
        #bob_ka = int((x**Bob_priv_key)%P)
        #return bob_ka


while True:
    # input message we want to send to the server
    to_send =  input("Enter command: ")
    # a way to exit the program
    if to_send.lower() == 'quit':
        break

    elif to_send.lower() == 'sendmypublickey':
        to_send = get_key(priv_key)

    elif to_send.lower() == 'getsecretkey':
        x = int(input("Enter public key of other: "))

        secret_key = get_secret(priv_key, x)
        print("Secret key: ", secret_key)

        sys.exit() # quit program since secret key computed

    # add the datetime, name & the color of the sender
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    to_send = f"{client_color}[{date_now}] {name}{separator_token}{to_send}{Fore.RESET}"
    # finally, send the message
    s.send(to_send.encode())

# close the socket
s.close()