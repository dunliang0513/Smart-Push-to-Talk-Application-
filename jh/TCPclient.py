# Demo Simple TCP Echo Client
# (c) Author: Bhojan Anand
# Last Modified: 2023 Sep
# Course: CS3103/CS2105
# School of Computing, NUS
# Note: Code does not follow best pratices such as exception handling etc.

import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
name = input('Please enter your name: ')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Connect to the host, post
    s.connect((HOST, PORT))

    # Define the data to be sent
    senddata = input(f"Enter message: ")
    while senddata:
        senddata = f'{name}: {senddata}'
        # Encoding the data as UTF-8 as bytes
        senddatabytes = senddata.encode(encoding = 'UTF-8')
        # print("Data to send: " , senddatabytes)

        s.sendall(senddatabytes)

        # recvdata is the data received from server
        recvdata = s.recv(1024) 
        print(f"Received {recvdata}")  #formatted string, includes substituions python 3.6 and above
        senddata = input("Your data:")
    s.close()