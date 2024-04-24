# Client Camera and Screen Viewer

This script enables the utilization of the client's camera and screen.

Upon building client.pyw, it operates within background processes.

## Change log for version 4v:
- Redesigned the system of IDs; now clients are assigned a 4-digit random number upon application start instead of sequential numbering.
- Redesigned the main menu for improved clarity, displaying available pages and connected clients.
- Redesigned the system for displaying clients, increasing the capacity from a maximum of 2 to at least 100.
- Ongoing redesign of the client system to include a debugging console.
- Added functionality to display a screenshot when no camera is detected.
- Implemented a debugging page to facilitate error detection by displaying all variables in the code.
- Fixed console spam when accessing the page of a disconnected client.

## Tutorial:

1. Set up a Python server.
2. Upload the server.py file and the templates folder to the server.
3. Change the port in the last line of server.py to match your server's port.
4. In line 7 of client.pyw, replace '127.0.0.1:5000' with your server's IP address and port.
5. Start your server and build client.pyw (e.g., using pyinstaller).
6. Share the generated client.exe file with your friend.

### Requirements.txt for server:
```python
Flask
opencv-python
numpy
```

### How to close:
1. Use the task manager to end the client.exe process (or its equivalent).
2. Restart your computer.

### Known issues:
None reported.

# DISCLAIMER: THIS IS FOR EDUCATIONAL PURPOSES ONLY.
