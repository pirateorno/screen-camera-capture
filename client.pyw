import cv2
import requests
import pyautogui
import numpy as np
from PIL import Image

# Write here your server ip
remote_server = '127.0.0.1:5000'

# camera initialization
try:
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
except Exception as e:
    camera = cv2.VideoCapture('NoCamera.avi')
    print(e)



while True:
    if camera:
        success, frame = camera.read()
        if not success or frame is None:
            break

    myScreenshot = pyautogui.screenshot()
    myScreenshot_np = np.array(myScreenshot)


    # images to .jpg
    _, img_encoded = cv2.imencode('.jpg', frame)
    _, screen_encoded = cv2.imencode('.jpg', myScreenshot_np)

    # sending frames to server
    img_response = requests.post(f'http://{remote_server}/send_camera', data=img_encoded.tobytes(), headers={'Content-Type': 'image/jpg'})
    screen_response = requests.post(f'http://{remote_server}/send_screen', data=screen_encoded.tobytes(), headers={'Content-Type': 'image/jpg'})

    if img_response.status_code != 200:
        print(f"Error when sending a frame to the server: {img_response.status_code}")
    if screen_response.status_code != 200:
        print(f"Error when sending a screenshot to the server: {screen_response.status_code}")

if camera:
    camera.release()
