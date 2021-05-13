import socket 
import threading
import sys 
import select

MSG_SIZE = 1024
IP = sys.argv[1]
PORT = int(sys.argv[2])
ADDR = (IP, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
clients_list = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)

def handle_client(clt, addr):
    print(f"Connected to {addr}")
    clt.send("CONNECTED SUCCESSFULLY".encode(FORMAT))
    while True:
        msg = clt.recv(MSG_SIZE).decode(FORMAT)
        # print(f"message being sent :{msg};; from [{addr}] ")
        if msg == DISCONNECT_MESSAGE:
            print('\n *** DISCONNECTING *** \n')
            clt.send("\n *** DISCONNECTING *** \n".encode(FORMAT)) #confrimation to client
            if clt in clients_list:
                clients_list.remove(clt)
            break
        
        elif msg:
            # clt.send("\n Message Sent \n".encode(FORMAT)) #confrimation to client
            for rcpt in clients_list:
                if rcpt != clt:
                    rcpt.send(f"[{addr}] sent :>    {msg}".encode(FORMAT))
                    
        else:
            clt.send("\n MESSAGE NOT SENT \n".encode(FORMAT)) #alert client

    clt.close()
    
def startServer():
    server.listen(3)
    print(f"[LISTENING] Server is listening on {IP}")
    while True:
        clt, addr = server.accept()
        clients_list.append(clt)
        handle = threading.Thread(target=handle_client, args=(clt, addr)).start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

    
print("[STARTING] server is starting...")
startServer()
