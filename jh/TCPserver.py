# Demo Simple TCP Echo Server - MultiThreaded 
# (c) Author: Bhojan Anand
# Last Modified: 2023 Sep
# Course: CS3103/CS2105
# School of Computing, NUS
# Note: Code does not follow best pratices such as exception handling etc.

import socket               
from threading import Thread  

whoIsTalking = ''

def on_new_client(clientsocket,addr):
    if whoIsTalking == '' or whoIsTalking == addr:
        while True:
            received_message = clientsocket.recv(1024)
            if not received_message: break
            # print (addr, ' >> ', received_message)

            # Decoding
            received_message_Str = received_message.decode()
            name, data = received_message_Str.split(': ', 1)
            name = name.strip()
            data = data.strip()
            server_response = f'Message received from {name} {addr}: {data}'
            print(server_response)
            replyMsgBytes = server_response.encode()
            clientsocket.sendall(replyMsgBytes)
        clientsocket.close()
        print ('connection closed for',  addr )

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # s is LISTENING Socket
host = "127.0.0.1"   
port = 65432                # Reserve a port for your service.

s.bind((host, port))        # Bind to the port
s.listen(100)                 # Max 100 concurrent connections
print ('Server started!')
print ('Waiting for clients...')

while True:
   c, addr = s.accept()  # WAIT for client connection. Establish connection with client. c is CONNECTION Socket
   print (f'Connection received from {addr}')
   thread = Thread(target=on_new_client, args=(c, addr))  # create the thread
   thread.start()  # start the thread
   s.close() # - always ON server
   
