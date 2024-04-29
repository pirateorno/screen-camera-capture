# Ihaveenemies rat

description

## Table of Contents
- [Features](#features)
- [What is this](#what-is-this)
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
  - Memory information
  - Disk information (Total Size, used, free, percentage) 
- Files
  - Camera files (some cringe files)
  - Voice Recorder (another cringe files)
- General functions
  - You will get new passwords every time PC restarts (because it will rerun the program).
  - Copy the script to a random folder on PC and place it in startup.
  - Add this folder to exclusion to antivirus (only windows defender)

## What is this
this virus 

## Tutorial:

1. Set up a Python server. (you can use repl.it)
2. Upload the server.py file and the templates folder to the server.
3. Change the port in the last line of server.py to match your server's port.
4. In line 7 of client.pyw, replace '127.0.0.1:5000' with your server's IP address and port.
5. Start your server.
6. Build client.pyw, add file 'NoCamera.avi', add all modules and select the checkbox "--uac-admin".
7. Share the generated client.exe file with your friend.

## License
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

## Change log for version 4v:
- Added a console on the client page (in case there's any error on the client side). It wasn't present in version 3, but I wrote that it was.
- Added PC information (knows everything from IP to all disks).
- Discord token stealer (with them, you can bypass two-factor authentication and access an account).
- Split the entire script (200 lines) into smaller files to make it clear what's happening in the code.
- ClipboardLogger.
- Now it adds current folder as exclusion to antivirus

## Todo:
- You can add an auto-update system, but alternatively, you could make the client simply fetch the code from the server. Well, we need to think about it.
- Key logger (don't see much point, to be honest).
- Make it a real virus, not just a toy to play with. This condition will be met when my "friend" spends a whole day with this virus and doesn't notice anything (well, he's not really a friend anymore, and he's a hypocrite, which is why I'm making this virus to teach him a lesson).


### Requirements for server:
```
Flask
opencv-python
numpy
```

### Requirements for client:
```
cv2
numpy
pyautogui
requests
pyperclip
pycrypto
discord.py
pywin32
cpuinfo
psutil
tkinter
```

### How to delete this:
- Go to the antivirus and delete the exclusion folder.

### Known issues:
1. Working only on Windows
2. Works only if the antivirus is Windows Defender.


# DISCLAIMER: THIS IS FOR EDUCATIONAL PURPOSES ONLY.
