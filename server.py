import socket
import threading
PORT=5050
HEADER=64
FORMAT='utf-8'
DISCONNET_MESSAGE = "!DICONNECT"
#Get the ip address of this computer
SERVER=socket.gethostbyname(socket.gethostname())
ADDR=(SERVER,PORT)
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNET_MESSAGE:
                connected = False
            print(f"[{addr}] {msg}")
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