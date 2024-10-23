# CS3103 Group Assignment 4 - Smart Push-to-Talk Application for Class Discussion (Using TCP Socket)

The goal of this assignment is to design and implement a Push-to-Talk (PTT) web 
application using TCP Socket. The application will allow multiple clients (students) to press
a button to stream live audio (their voice) to a server (instructor’s machine). This is a oneway 
streaming system, where the audio is streamed from the client to the server for verbal
discussion in a large class. The assignment will focus on TCP Socket for real-time
communication, audio streaming, and handling multiple client connections in a simple,
interactive way.

### TCP Client (Student’s Device):
* The client will capture the microphone input (using the Web Audio API or any
platform-specific microphone input library) and send the audio data over a TCP
connection to the server.
* Audio data can be encoded using a simple codec (like PCM, Opus, or MP3) to
reduce bandwidth and then streamed over the TCP connection.
 
### TCP Server (Professor’s Device):
* The server will receive the audio stream, decode it if necessary, and play it on the
system's speakers in real-time.
* The server should be capable of managing multiple connections and enforcing the
rule that only one client can speak at a time (First-Come-First-Served basis). [Single
threaded/process simple TCP server is sufficien