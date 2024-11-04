# Smart Push-to-Talk Web Application

This project is a real-time, web-based Push-to-Talk (PTT) voice communication system. It consists of a client-side HTML application (`ptt.html`) and a server-side Python script (`server.py`). The system allows one client to connect and stream audio to the server at a time, with other clients being notified if they cannot connect or speak. Built with WebSockets for low-latency audio streaming, it is designed to be simple, reliable, and efficient.


## Features

- **Push-to-Talk Button**: Allows clients to stream audio to the server by pressing and holding a button.
- **Audio Streaming**: Captures voice from the client's microphone and transmits it via WebSockets to the server.
- **Concurrency Control**: Only one client can connect and speak at a time. If another client tries to connect, they will be denied access.
- **Error Handling and Client Feedback**: Provides real-time feedback and error messages if multiple clients attempt to connect or if a disconnection occurs.
- **Server Log Monitoring**: The server logs connection attempts, disconnections, and status changes, showing which client currently has speaking rights.

## Architecture

The application consists of two main components:

1. **Client-Side Application (`ptt.html`)**:
   - Captures audio from the user’s microphone using the Web Audio API.
   - Connects to the server via WebSockets to transmit audio data.
   - Provides a user interface for connecting, disconnecting, and using the Push-to-Talk button.

2. **Server-Side Application (`server.py`)**:
   - A WebSocket server that listens for audio data from clients.
   - Plays received audio using the `pyaudio` library.
   - Manages concurrency by allowing only one client to connect and speak at a time.
   - Logs client connection attempts and disconnections for monitoring.

## Requirements

- **Python 3.x**
- **Node.js (optional)** if you want to serve the HTML file locally with a simple HTTP server.
- **Python Packages**:
  - `pyaudio`
  - `websockets`
  - `asyncio`

## Setup

### Linux/Mac Setup

1. Clone the repository and navigate to the source directory:

   ```bash
   git clone https://github.com/your-username/Smart-Push-to-Talk-Web-Application.git
   cd Smart-Push-to-Talk-Web-Application/src
   ```

2. Run the environment setup script:

   ```bash
   ./env_setup.sh
   ```

   This will create a virtual environment, activate it, and install the required packages.

3. Activate the virtual environment (if not already activated):

   ```bash
   source venv/bin/activate
   ```

4. Determine the server's IP address by running:

   ```bash
   ifconfig
   ```

   Note the `inet` address under your active network interface.

5. Open `server.py` and update the `HOST` variable with your server IP address:

   ```python
   HOST = "your_server_ip_address"
   ```

6. Start the server:

   ```bash
   python server.py
   ```

### Windows Setup

1. Clone the repository and navigate to the source directory:

   ```cmd
   git clone https://github.com/your-username/Smart-Push-to-Talk-Web-Application.git
   cd Smart-Push-to-Talk-Web-Application\src
   ```

2. Run the environment setup script:

   ```cmd
   env_setup.bat
   ```

   This will create a virtual environment, activate it, and install the required packages.

3. Activate the virtual environment (if not already activated):

   ```cmd
   venv\Scripts\activate
   ```

4. Determine the server's IP address by running:

   ```cmd
   ipconfig
   ```

   Note the IPv4 address.

5. Open `server.py` and update the `HOST` variable with your server IP address:

   ```python
   HOST = "your_server_ip_address"
   ```

6. Start the server:

   ```cmd
   python server.py
   ```

## Usage

### Running the Client

1. **Open `ptt.html`**:
   - Open the `ptt.html` file in a web browser (e.g., Chrome, Firefox, or Edge). You can either open the file directly or serve it using a local HTTP server.

   ```bash
   # If you have Node.js, you can serve it locally:
   npx http-server -p 8080
   ```

2. **Enter Connection Information**:
   - Enter your name, the server IP address, and the port number (default: `65432`).

3. **Connect**:
   - Click the **Connect** button to establish a WebSocket connection with the server.
   - If another client is already connected, you will see a message indicating you cannot connect.

4. **Use Push-to-Talk**:
   - Once connected, press and hold the **Press and Hold to Talk** button to stream audio.
   - Release the button to stop streaming.

5. **Disconnect**:
   - Click the **Disconnect** button to terminate the connection with the server.

### Firewall and Network Settings

- Ensure both the server and client are on the same Wi-Fi network and that firewall settings allow communication over the specified port (default: `65432`).


---

Make sure to update the placeholder GitHub link and the IP address placeholder instructions with the correct details before adding this to your repository. This README provides a comprehensive overview of the project for anyone interested in using or contributing to it.
