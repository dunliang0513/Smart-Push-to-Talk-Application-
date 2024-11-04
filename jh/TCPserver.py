# import socket
# import pyaudio

# HOST = "172.31.69.15"
# PORT = 65432

# # Initialize PyAudio
# audio = pyaudio.PyAudio()

# # Open an output stream to play audio
# stream = audio.open(format=pyaudio.paInt16,
#                     channels=1,
#                     rate=44100,
#                     output=True)

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen(1)  # Limit to 1 incoming connection at a time
#     print("Server listening on port", PORT)

#     while True:
#         # Wait for a client to connect
#         conn, addr = s.accept()
#         print("Connected by", addr)
#         with conn:
#             try:
#                 while True:
#                     data = conn.recv(1024)
#                     if not data:
#                         break
#                     # Play the received audio data
#                     stream.write(data)
#             except ConnectionResetError:
#                 print("Client disconnected abruptly")
#             finally:
#                 print("Client disconnected. Waiting for a new connection...")

# # Cleanup (will only happen if you stop the server manually)
# stream.stop_stream()
# stream.close()
# audio.terminate()

import socket
import threading
import pyaudio

HOST = "172.31.69.15"
PORT = 65432

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open an output stream to play audio
stream = audio.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    output=True)

# Flag to indicate if a client is connected
client_connected = False
lock = threading.Lock()

def handle_client(conn, addr):
    global client_connected
    print("Connected by", addr)
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            # Play the received audio data
            stream.write(data)
    except ConnectionResetError:
        print("Client disconnected abruptly")
    finally:
        print("Client disconnected. Waiting for a new connection...")
        conn.close()
        with lock:
            client_connected = False

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Server listening on port", PORT)

    while True:
        conn, addr = s.accept()
        with lock:
            if not client_connected:
                client_connected = True
                # Start a new thread to handle the client
                client_thread = threading.Thread(target=handle_client, args=(conn, addr))
                client_thread.start()
            else:
                # Send message to client and close connection
                message = "Another client is connected. Please try again later."
                conn.sendall(message.encode())
                conn.close()

# Cleanup (will only happen if you stop the server manually)
stream.stop_stream()
stream.close()
audio.terminate()
