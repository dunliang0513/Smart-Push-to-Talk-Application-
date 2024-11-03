import asyncio
import websockets
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

async def handle_client(websocket, path):
    print("Client connected")
    try:
        async for message in websocket:
            # Write received audio data to output stream
            stream.write(message)
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

async def main():
    async with websockets.serve(handle_client, HOST, PORT):
        print(f"Server listening on ws://{HOST}:{PORT}")
        await asyncio.Future()  # Run forever

try:
    asyncio.run(main())
finally:
    # Cleanup PyAudio resources when the server is stopped
    stream.stop_stream()
    stream.close()
    audio.terminate()
