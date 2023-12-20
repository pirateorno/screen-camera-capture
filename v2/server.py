from flask import Flask, request, Response, render_template, jsonify
import cv2
import numpy as np

app = Flask(__name__)
last_frame = None
screen_last_frame = None

@app.route('/video_feed', methods=['GET', 'POST'])
def video_feed():
    global last_frame
    if request.method == 'POST':
        frame_data = request.data  # Получаем данные кадра от клиента

        # Здесь вы можете обработать frame_data по вашему усмотрению, например, преобразовать из байтов в изображение

        # Преобразуем данные кадра в изображение (пример, если данные в формате JPEG)
        frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)

        if frame is not None:
            last_frame = frame  # Сохраняем последний полученный кадр

        # Отправляем ответ обратно клиенту
        return Response(status=200)

    return render_template('../clients/../templates/client1.html')

@app.route('/get_video_frame', methods=['GET'])
def get_video_frame():
    global last_frame
    if last_frame is not None:
        _, encoded_frame = cv2.imencode('.jpg', last_frame)
        return Response(encoded_frame.tobytes(), mimetype='image/jpeg')

    return "No frame available"

@app.route('/screen_feed', methods=['GET', 'POST'])
def screen_feed():
    global screen_last_frame
    if request.method == 'POST':
        frame_data = request.data  # Получаем данные кадра от клиента

        # Здесь вы можете обработать frame_data по вашему усмотрению, например, преобразовать из байтов в изображение

        # Преобразуем данные кадра в изображение (пример, если данные в формате JPEG)
        frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)

        if frame is not None:
            screen_last_frame = frame  # Сохраняем последний полученный кадр

        # Отправляем ответ обратно клиенту
        return Response(status=200)

@app.route('/get_screen_frame', methods=['GET'])
def get_screen_frame():
    global screen_last_frame
    if screen_last_frame is not None:
        _, encoded_frame = cv2.imencode('.jpg', screen_last_frame)
        return Response(encoded_frame.tobytes(), mimetype='image/jpeg')

    return "No frame available"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
