# client.py
import socket
import subprocess
import signal
import sys
import shutil
import time

class VoiceClient:
    def __init__(self, server_ip, port=8000):
        self.server_ip = server_ip
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

    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.server_ip, self.port))
            print(f"Connected to server at {self.server_ip}:{self.port}")
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False

    def start_streaming(self):
        self.running = True
        try:
            print("Initializing FFmpeg...")
            # List available audio devices
            list_devices = subprocess.Popen(
                ['ffmpeg', '-list_devices', 'true', '-f', 'dshow', '-i', 'dummy'],
                stderr=subprocess.PIPE
            )
            devices_output = list_devices.stderr.read().decode()
            print("Available audio devices:")
            print(devices_output)
            
            print("Starting audio capture...")
            self.process = subprocess.Popen(
                ['ffmpeg', '-f', 'dshow',
                 '-i', 'audio=Microphone Array (AMD Audio Device)',
                 '-acodec', 'pcm_s16le',  # Use PCM format
                 '-ar', '44100',          # Sample rate
                 '-ac', '2',              # Stereo
                 '-f', 'wav',             # WAV format
                 '-'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=4096
            )
            
            print("Started audio streaming. Speaking into microphone...")
            
            # Check for immediate FFmpeg errors
            time.sleep(1)  # Give FFmpeg a moment to start
            if self.process.poll() is not None:
                error_output = self.process.stderr.read().decode()
                print(f"FFmpeg failed to start: {error_output}")
                return
            
            print("FFmpeg process started successfully")
            
            while self.running:
                # Check if FFmpeg is still running
                if self.process.poll() is not None:
                    error_output = self.process.stderr.read().decode()
                    print(f"FFmpeg process terminated unexpectedly: {error_output}")
                    break
                
                data = self.process.stdout.read(1024)
                if not data:
                    print("No data received from FFmpeg")
                    break
                    
                try:
                    self.sock.sendall(data)
                    print(".", end="", flush=True)  # Progress indicator
                except socket.error as e:
                    print(f"\nSocket error: {e}")
                    break
                
        except Exception as e:
            print(f"Streaming error: {e}")
            if self.process and self.process.stderr:
                error_output = self.process.stderr.read().decode()
                print(f"FFmpeg error output: {error_output}")
        finally:
            self.stop()

    def start(self):
        if not self.check_ffmpeg():
            return

        if not self.connect():
            return

        def signal_handler(sig, frame):
            print("\nStopping stream...")
            self.stop()
            sys.exit(0)
            
        signal.signal(signal.SIGINT, signal_handler)
        self.start_streaming()

    def stop(self):
        print("\nStopping client...")
        self.running = False
        if self.process:
            print("Terminating FFmpeg process...")
            self.process.terminate()
            self.process.wait()  # Wait for process to terminate
            print("FFmpeg process terminated")
        if self.sock:
            try:
                print("Closing socket connection...")
                self.sock.shutdown(socket.SHUT_RDWR)
            except:
                pass
            self.sock.close()
            print("Socket connection closed")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python client.py SERVER_IP")
        sys.exit(1)
        
    client = VoiceClient(sys.argv[1])
    client.start()