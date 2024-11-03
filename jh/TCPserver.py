import socket
import pyaudio

HOST = "127.0.0.1"
PORT = 65432

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open an output stream to play audio
stream = audio.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    output=True)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)  # Limit to 1 incoming connection at a time
    print("Server listening on port", PORT)

    while True:
        # Wait for a client to connect
        conn, addr = s.accept()
        print("Connected by", addr)
        with conn:
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

# Cleanup (will only happen if you stop the server manually)
stream.stop_stream()
stream.close()
audio.terminate()
