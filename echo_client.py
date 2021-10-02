import socket
from scratchio.scheduler import Scheduler

HOST = 'localhost'    # The remote host
PORT = 50007          # The same port as used by the server

scheduler = Scheduler()

async def connect_client(i):
    with socket.socket() as client_socket:
        client_socket.connect((HOST, PORT))
        print(i, "Sending ...")
        client_socket.sendall(b'Hello, world')
        print(i, "Sleeping ...")
        await scheduler.sleep(0)
        data = client_socket.recv(1024)
    print(i, 'Received', repr(data))


for i in range(5):
    scheduler.call_soon(connect_client(i))
        
scheduler.run()