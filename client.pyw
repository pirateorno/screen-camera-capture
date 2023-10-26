import cv2
import requests
import pyautogui
from PIL import Image
import numpy as np

# URL удаленного сервера, на который будет отправляться видеопоток
remote_server_camera_url = 'http://IP:PORT/video_feed'
remote_server_screen_url = 'http://IP:PORT/screen_feed'

# Инициализация камеры
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    success, frame = camera.read()
    myScreenshot = pyautogui.screenshot()

    # Convert the PIL image to a NumPy array
    myScreenshot_np = np.array(myScreenshot)

    #myScreenshot.save(r'screenshot.jpg')
    if not success:
        break

    # Преобразование кадра в формат JPEG
    _, img_encoded = cv2.imencode('.jpg', frame)
    _, screen_encoded = cv2.imencode('.jpg', myScreenshot_np)  # Use the NumPy array

    # Отправка кадра на удаленный сервер
    img_response = requests.post(remote_server_camera_url, data=img_encoded.tobytes(), headers={'Content-Type': 'image/jpg'})
    screen_response = requests.post(remote_server_screen_url, data=screen_encoded.tobytes(), headers={'Content-Type': 'image/jpg'})

    if img_response.status_code != 200:
        print(f"Ошибка при отправке кадра на сервер: {img_response.status_code}")
    if screen_response.status_code != 200:
        print(f"Ошибка при отправке скрина на сервер: {screen_response.status_code}")

# Закрыть камеру
camera.release()
