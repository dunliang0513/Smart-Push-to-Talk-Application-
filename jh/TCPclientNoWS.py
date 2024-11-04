# import socket
# import pyaudio

# HOST = "127.0.0.1"
# PORT = 65432

# # Initialize PyAudio
# audio = pyaudio.PyAudio()
# stream = audio.open(format=pyaudio.paInt16,
#                     channels=1,
#                     rate=44100,
#                     input=True,
#                     frames_per_buffer=1024)

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     print("Connected to server")

#     try:
#         while True:
#             # Read audio data from the microphone
#             print("Reading audio data from the microphone")
#             data = stream.read(1024, exception_on_overflow=False)
#             # Send audio data to the server
#             print("Sending data to the server")
#             s.sendall(data)
#     except KeyboardInterrupt:
#         print("Stopped by user")

# # Cleanup
# stream.stop_stream()
# stream.close()
# audio.terminate()


import socket
import time
import pyaudio

HOST = "172.31.69.15"
PORT = 65432

# Initialize PyAudio
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=1024)

def connect_to_server():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            print("Connected to server")

            # Check for any immediate message from the server
            s.settimeout(1.0)  # Set a timeout for receiving data
            try:
                message = s.recv(1024).decode()
                if message == "Another client is connected. Please try again later.":
                    print("Server is busy. Retrying in 5 seconds...")
                    s.close()
                    time.sleep(5)
                    continue  # Try to connect again
                else:
                    # Unexpected message, proceed with caution
                    print("Received unexpected message from server:", message)
            except socket.timeout:
                # No immediate message from server, proceed to send audio data
                pass

            # Reset timeout
            s.settimeout(None)

            # Start sending audio data
            try:
                while True:
                    # Read audio data from the microphone
                    data = stream.read(1024, exception_on_overflow=False)
                    # Send audio data to the server
                    s.sendall(data)
            except KeyboardInterrupt:
                print("Stopped by user")
                break
            except Exception as e:
                print("Connection error:", e)
                break
            finally:
                s.close()
        except ConnectionRefusedError:
            print("Cannot connect to server. Retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            print("An error occurred:", e)
            time.sleep(5)

    # Cleanup
    stream.stop_stream()
    stream.close()
    audio.terminate()

if __name__ == "__main__":
    connect_to_server()
