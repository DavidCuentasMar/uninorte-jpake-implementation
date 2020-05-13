import socket
from jpake import JPAKE
import pickle
import json

class ZPK:
    def __init__(self, g,b,id):
        self.g = g
        self.b = b
        self.id = id

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER=socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
client_custom_id = "1s"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
jpake_configured = False
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

def jpake_send(msg):
    message = msg
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
    print('Setting Up JPAKE...')
    secret = "1234"
    alice = JPAKE(secret=secret, signer_id=client_custom_id)
    zpkObj = ZPK(alice.zkp_x1['gr'],alice.zkp_x1['b'],alice.zkp_x1['id'])
    zpkObj_string = pickle.dumps(zpkObj)
    if(jpake_configured==False):
        send('JPAKE_SETTING_UP')
        jpake_send(zpkObj_string)
    input()
    #client_msg = input('=> ')
    #send(client_msg)
send(DISCONNECT_MESSAGE)