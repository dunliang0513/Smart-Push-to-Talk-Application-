# server.py
import socket
import subprocess
import signal
import sys
import shutil

class VoiceServer:
    def __init__(self, host='127.0.0.1', port=8000):  # Changed to localhost
        self.host = host
        self.port = port
        self.sock = None
        self.process = None
        self.running = False

    def check_ffmpeg(self):
        if shutil.which('ffmpeg') is None:
            print("Error: FFmpeg is not installed or not in PATH")
            print("Please install FFmpeg and add it to your system PATH")
            return False
        return True

    def setup_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.sock.bind((self.host, self.port))
            self.sock.listen(5)
            print(f"Server listening on {self.host}:{self.port}")
        except Exception as e:
            print(f"Failed to bind socket: {e}")
            sys.exit(1)

    def handle_client(self, conn, addr):
        print(f"Client connected from {addr}")
        try:
            print("Starting FFmpeg process...")
            self.process = subprocess.Popen(
                ['ffmpeg',
                 '-f', 'wav',        # Input format is WAV
                 '-i', '-',          # Read from pipe
                 '-acodec', 'pcm_s16le',  # Output codec
                 '-ar', '44100',     # Sample rate
                 '-ac', '2',         # Stereo
                 '-af', 'volume=1.5',# Increase volume
                 '-f', 'directsound',# Output to DirectSound
                 'default'],         # Default audio device
                stdin=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=4096
            )
            
            print("Ready to receive audio...")
            
            # Buffer for WAV header
            header_size = 44  # Standard WAV header size
            header_received = False
            header_data = bytearray()
            
            while self.running:
                try:
                    data = conn.recv(1024)
                    if not data:
                        print("Client disconnected")
                        break
                    
                    if not header_received:
                        # Collect header data
                        header_data.extend(data[:header_size - len(header_data)])
                        if len(header_data) >= header_size:
                            # We have the complete header
                            self.process.stdin.write(header_data)
                            self.process.stdin.flush()
                            # Write remaining data if any
                            if len(data) > header_size - len(header_data):
                                self.process.stdin.write(data[header_size - len(header_data):])
                                self.process.stdin.flush()
                            header_received = True
                    else:
                        self.process.stdin.write(data)
                        self.process.stdin.flush()
                    
                    print(".", end="", flush=True)  # Progress indicator
                    
                except socket.error as e:
                    print(f"\nSocket error: {e}")
                    break
                    
        except Exception as e:
            print(f"\nError: {e}")
            if self.process and self.process.stderr:
                error_output = self.process.stderr.read().decode()
                print(f"FFmpeg error output: {error_output}")
        finally:
            print("\nCleaning up connection...")
            if self.process:
                try:
                    print("Terminating FFmpeg process...")
                    self.process.stdin.close()
                    self.process.terminate()
                    self.process.wait()
                    print("FFmpeg process terminated")
                except:
                    pass
            conn.close()
            print("Connection closed")

    def start(self):
        if not self.check_ffmpeg():
            return

        self.running = True
        self.setup_socket()
        
        def signal_handler(sig, frame):
            print("\nShutting down server...")
            self.stop()
            sys.exit(0)
            
        signal.signal(signal.SIGINT, signal_handler)
        
        try:
            while self.running:
                conn, addr = self.sock.accept()
                self.handle_client(conn, addr)
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.stop()

    def stop(self):
        print("\nStopping server...")
        self.running = False
        if self.sock:
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
            except:
                pass
            self.sock.close()
            print("Server socket closed")
        if self.process:
            self.process.terminate()
            self.process.wait()
            print("FFmpeg process terminated")

if __name__ == "__main__":
    server = VoiceServer()
    server.start()