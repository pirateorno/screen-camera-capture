from flask import Flask, request, Response, render_template
import cv2
import numpy as np

app = Flask(__name__)
last_frame = None
screen_last_frame = None

clientsnum = 0
clients = {}

@app.route('/', methods=['GET'])
def mainSite():
    return render_template('main.html')

@app.route('/clients/client1', methods=['GET'])
def client1():
    return render_template('client1.html')

@app.route('/client', methods=['GET', 'POST'])
def regclient():
    global clientsnum
    global clients

    if request.method == 'POST':
        if not request.remote_addr in clients:
            clientsnum += 1
            clients[request.remote_addr] = clientsnum

    return Response(str(clientsnum))

@app.route('/send_camera', methods=['GET', 'POST'])
def send_camera():
    global last_frame
    if request.method == 'POST':
        frame_data = request.data
        frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)
        if frame is not None:
            last_frame = frame

        return Response(status=200)

@app.route('/get_camera_frame', methods=['GET'])
def get_camera_frame():
    global last_frame
    if last_frame is not None:
        _, encoded_frame = cv2.imencode('.jpg', last_frame)
        return Response(encoded_frame.tobytes(), mimetype='image/jpeg')

    return "No frame available"

@app.route('/send_screen', methods=['GET', 'POST'])
def send_screen():
    global screen_last_frame
    if request.method == 'POST':
        frame_data = request.data
        frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)

        if frame is not None:
            screen_last_frame = frame

        return Response(status=200)

@app.route('/get_screen_frame', methods=['GET'])
def get_screen_frame():
    global screen_last_frame
    if screen_last_frame is not None:
        _, encoded_frame = cv2.imencode('.jpg', screen_last_frame)
        return Response(encoded_frame.tobytes(), mimetype='image/jpeg')

    return "No frame available"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=20015)
