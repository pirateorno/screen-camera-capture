# This script allows you to use the client's camera and screen.

If you build client.pyw, it will run in the background processes.

  

### Tutorial:

1. You need a python server.
2. You need to upload the server.py file and the templates folder to the server
3. Then on line 65 of server.py change the port to your server's port
 Example:
```python
app.run(host='0.0.0.0', port=20015)
```
4. In the 8th line of client.pyw, replace SERVERIP:PORT with ip:port/video_feed of your server.
5. On line 9 of client.pyw, change SERVERIP:PORT to ip:port/screen_feed of your server.
 Example:
```python
remote_server_camera_url = 'http://verycoolIP:20015/video_feed'
remote_server_screen_url = 'http://verycoolIP:20015/screen_feed'
```
6. Start your server and build client.pyw
7. Send client.exe to your friend

### requirements.txt for server:
```python
Flask==3.0.0
opencv-python==4.8.1.78
blinker==1.6.2
itsdangerous==2.1.2
MarkupSafe==2.1.3
Jinja2==3.1.2
click==8.1.7
watchdog==3.0.0
Werkzeug==3.0.0
Pillow==10.0.1
```


### How to close it, 2 ways:
1. In the task manager, close client.exe (or something similar)
2. Restart your computer.

### Some errors:
1. If client don't have a camera, the program will not work
2. If client have bad internet, the prpgram will not work
3. if client dont have camera program will not work
4. if client.exe (client.py or client.pyw) is opened by two or more users, the program will not work (I think I will not fix it)

That's all, sorry for my bad English.
# AND REMEMBER THIS IS FOR EDUCATIONAL PURPOSES ONLY.
