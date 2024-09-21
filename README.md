# DISCLAIMER: THIS IS FOR EDUCATIONAL PURPOSES ONLY.

# Simple rat
## Table of Contents
- [Features](#features)
- [What is this](#)
- [Tutorial](#tutorial)
- [License](#license)

## Features
- Discord information
  - Email
  - Phone
  - Gift codes
  - Billing
  - HQ Guilds
  - Token
- Pc information
  - System
  - Processor 
  - Ip-address
  - Mac-address
  - Boot time
  - Antivirus name
  - Memory information
  - Disk information (Total Size, used, free, percentage) 
- Files (not working)
  - Camera files (some cringe files)
  - Voice Recorder (another cringe files)
- Stealer (Chrome, edge, opera Gx)
  - password stealer
  - cookie stealer
- Other
  - Add virus to startup startup.
  - Add virus folder to exclusion to antivirus (only windows defender)

## Tutorial:

1. Set up a Python server. (like repl.it or similar)
2. Upload the server.py and templates folder to the server
3. Change the port in the last line of server.py to match your server's port
4. In line 30 of client.pyw, replace '127.0.0.1:5000' with your server's IP address and port
5. Start your server
6. Build client.pyw, add file 'NoCamera.avi', all modules and then add "--uac-admin"
7. Share the generated client.exe file with your "friend"

## Change log for version 4v:
- Added PC information
- Discord token stealer (with them, you can bypass two-factor authentication and access an account)
- Split the entire script into smaller files
- ClipboardLogger
- Now it adds current folder as exclusion to antivirus

## Todo:
- You can add an auto-update system, but alternatively, you could make the client simply fetch the code from the server. Well, we need to think about it.
- Keylogger (don't see much point, to be honest).

## Requirements:
### Requirements for server:
```
Flask
Flask-SocketIO
opencv-python
numpy
```

### Requirements for client:
```
opencv-python
psutil
requests
python-socketio
Pillow
pyautogui
tendo
py-cpuinfo
pywin32
pyperclip
pycryptodome
discord.py
pypiwin32
```

### How to delete this:
1. Check task manager and close virus
2. Go to the antivirus and delete the exclusion folder.
3. Delete virus folder (you can find it when closing virus in task manager)

### Known issues:
1. Working only on Windows
2. Works only if the antivirus is Windows Defender.
3. 
## License
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
