import socket
import threading
import pyaudio
import websockets
import asyncio
import json
import logging
from websockets.exceptions import ConnectionClosed

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HOST = "172.31.50.171"
WS_PORT = 65432  # WebSocket port
CHUNK_SIZE = 1024

class AudioServer:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=44100,
            output=True
        )
        self.current_client = None
        self.lock = threading.Lock()
        
    async def handle_websocket(self, websocket, path):
        client_info = None
        try:
            # Wait for initial connection message with client name
            message = await websocket.recv()
            client_info = json.loads(message)
            client_name = client_info.get('name', 'Unknown')
            
            with self.lock:
                if self.current_client is None:
                    self.current_client = websocket
                    logger.info(f"Client {client_name} connected and has speaking rights")
                    await websocket.send(json.dumps({
                        "type": "status",
                        "status": "connected",
                        "canSpeak": True
                    }))
                else:
                    logger.info(f"Client {client_name} connected but cannot speak")
                    await websocket.send(json.dumps({
                        "type": "status",
                        "status": "connected",
                        "canSpeak": False,
                        "message": "Another client is currently speaking"
                    }))
                    return

            try:
                while True:
                    data = await websocket.recv()
                    if isinstance(data, bytes):
                        self.stream.write(data)
                    else:
                        logger.debug(f"Received non-binary message: {data}")
            except ConnectionClosed:
                logger.info(f"Client {client_name} disconnected")
            
        except Exception as e:
            logger.error(f"Error handling client: {str(e)}")
        finally:
            with self.lock:
                if self.current_client == websocket:
                    self.current_client = None
                    logger.info("Speaking rights released")

    async def start(self):
        async with websockets.serve(self.handle_websocket, HOST, WS_PORT):
            logger.info(f"WebSocket server started on ws://{HOST}:{WS_PORT}")
            await asyncio.Future()  # run forever

    def cleanup(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

if __name__ == "__main__":
    server = AudioServer()
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        logger.info("Server shutting down...")
        server.cleanup()