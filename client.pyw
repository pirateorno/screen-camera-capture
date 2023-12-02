import cv2
import requests
import pyautogui
import numpy as np

# Write here your server ip
remote_server = ''

# camera initialization
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    success, frame = camera.read()
    myScreenshot = pyautogui.screenshot()

    myScreenshot_np = np.array(myScreenshot)

    if not success:
        break

    # images to .jpg
    _, img_encoded = cv2.imencode('.jpg', frame)
    _, screen_encoded = cv2.imencode('.jpg', myScreenshot_np)  # Use the NumPy array

    # sending frames to server
    img_response = requests.post(f'http://{remote_server}/video_feed', data=img_encoded.tobytes(), headers={'Content-Type': 'image/jpg'})
    screen_response = requests.post(f'http://{remote_server}/screen_feed', data=screen_encoded.tobytes(), headers={'Content-Type': 'image/jpg'})

    if img_response.status_code != 200:
        print(f"Error when sending a frame to the server: {img_response.status_code}")
    if screen_response.status_code != 200:
        print(f"Error when sending a screenshot to the server: {screen_response.status_code}")

camera.release()
