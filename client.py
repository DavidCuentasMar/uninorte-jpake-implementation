import socket
from jpake import JPAKE
import pickle
import json


HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER=socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
client_custom_id = "1s"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

client_msg = ""
while client_msg != DISCONNECT_MESSAGE:
    if(client_custom_id == ""):
        client_custom_id = input(b'[SETUP - Client Custom ID] => ')
    client_custom_id = b"alice"
    client_msg = input('=> ')
    #send(client_msg)
    secret = "1234"
    alice = JPAKE(secret=secret, signer_id=client_custom_id)
    send(str(alice.zkp_x1['gr']))
send(DISCONNECT_MESSAGE)