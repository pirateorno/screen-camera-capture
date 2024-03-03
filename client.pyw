import cv2
import requests
import pyautogui
import numpy as np

# Define the IP address of the remote server
remote_server = '127.0.0.1:5000'

# Initialize the camera
try:
   camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Try to open the default camera
except Exception as e:
   camera = cv2.VideoCapture('NoCamera.avi')  # If no camera is available, use a backup video
   print(e)

# Request a client ID from the server
clientIdreq = requests.post(f'http://{remote_server}/client')
clientId = clientIdreq.text

while True:
   if camera:
       success, frame = camera.read()
       if not success or frame is None:
           break

   # Capture the current screen
   myScreenshot = pyautogui.screenshot()
   myScreenshot_np = np.array(myScreenshot)  # Convert the screenshot to a NumPy array

   # Encode the frames as .jpg
   _, camera_jpg = cv2.imencode('.jpg', frame)
   _, screen_jpg = cv2.imencode('.jpg', myScreenshot_np)

   # Send the frames to the server
   img_response = requests.post(f'http://{remote_server}/send_camera?id={clientId}', data=camera_jpg.tobytes(), headers={'Content-Type': 'image/jpg'})
   screen_response = requests.post(f'http://{remote_server}/send_screen?id={clientId}', data=screen_jpg.tobytes(), headers={'Content-Type': 'image/jpg'})

   if img_response.status_code != 200:
       print(f"Error when sending a frame to the server: {img_response.status_code}")
   if screen_response.status_code != 200:
       print(f"Error when sending a screenshot to the server: {screen_response.status_code}")

if camera:
   camera.release()