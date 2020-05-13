import socket
import threading
import pickle

PORT=5050
HEADER=64
FORMAT='utf-8'
DISCONNET_MESSAGE = "!DICONNECT"
#Get the ip address of this computer
SERVER=socket.gethostbyname(socket.gethostname())
ADDR=(SERVER,PORT)
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

all_clients = []
class ZPK:
    def __init__(self, g,b,id):
        self.g = g
        self.b = b
        self.id = id

def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    all_clients.append((conn,addr,False))    
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        for client_obj in all_clients:
            if client_obj[1]==addr and client_obj[2]==False:
                if msg_length:
                    msg_length = int(msg_length)            
                    msg = conn.recv(msg_length)
                    data_variable = pickle.loads(msg)          
                    print(f"[{addr}] {msg}")
                    print(data_variable)
            conn.send("Msg received".encode(FORMAT))

    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server IP: {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[SERVER STARTED]")
start()