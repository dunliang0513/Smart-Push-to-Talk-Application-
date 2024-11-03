import socket
import pyaudio

HOST = "127.0.0.1"
PORT = 65432

# Initialize PyAudio
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=1024)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Connected to server")

    try:
        while True:
            # Read audio data from the microphone
            print("Reading audio data from the microphone")
            data = stream.read(1024, exception_on_overflow=False)
            # Send audio data to the server
            print("Sending data to the server")
            s.sendall(data)
    except KeyboardInterrupt:
        print("Stopped by user")

# Cleanup
stream.stop_stream()
stream.close()
audio.terminate()
