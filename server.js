const express = require('express');
const WebSocket = require('ws');

const app = express();
const port = 3000;
const wss = new WebSocket.Server({ port: 3001 });

// Basic HTTP server setup
app.use(express.static('dist')); // Serve frontend files from 'dist'

app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});

// WebSocket setup for real-time audio data transfer
wss.on('connection', (ws) => {
    console.log('Client connected');

    ws.on('message', (message) => {
        console.log('Received audio data');
        // Here, you’d handle processing or playing the audio data
    });

    ws.on('close', () => {
        console.log('Client disconnected');
    });
});
