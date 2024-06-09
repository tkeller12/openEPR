import socket
import sys

import socketserver
from instrumentServer import MyServer, MyTCPHandler
from threading import Thread

HOST, PORT = "localhost", 9999
data = "Hello World!"

#server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
server = MyServer((HOST, PORT), MyTCPHandler)

t = Thread(target = server.serve_forever)
print('Starting Server...')
t.start()
print('Thread is alive:', t.is_alive())

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(bytes(data + "\n", "utf-8"))

    # Receive data from the server and shut down
    received = str(sock.recv(1024), "utf-8")

print("Sent:     {}".format(data))
print("Received: {}".format(received))

server.shutdown()
server.server_close()
del server
t.join()

print('thread is alive:', t.is_alive())
print('thread is alive:', t.is_alive())
del t
print('END')
