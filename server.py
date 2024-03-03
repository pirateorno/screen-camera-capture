from flask import Flask, request, Response, render_template
import cv2
import numpy as np
from random import randint

app = Flask(__name__)
last_frame = {}
screen_last_frame = {}

clients = {}

@app.route('/', methods=['GET'])
def mainSite():
    global clients
    return render_template('main.html', client = clients)

@app.route('/client/<int:clientId>', methods=['GET'])
def client1(clientId):
    return render_template(f'client.html', clientId = clientId)

@app.route('/client', methods=['GET', 'POST'])
def regclient():
    global clients

    clientId = 0

    if request.method == 'POST':
        if not request.remote_addr in clients:
            clientId = randint(1000,9999)
            clients[request.remote_addr] = {"clientId": clientId, "clientConsole": "hit the road Jack"}
        else:
            print(f"{request.remote_addr} arleady in clients!")

        return Response(str(clientId))

    if request.method == 'GET':
        return len(clients)

@app.route("/debug", methods=['GET'])
def debugpage():
    return f"Client: {clients}"

@app.route('/send_camera', methods=['GET', 'POST'])
def send_camera():
    global last_frame
    if request.method == 'POST':
        frame_data = request.data
        frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)
        if frame is not None:
            last_frame[request.args.get('id')] = frame

        return Response(status=200)

@app.route('/get_camera_frame', methods=['GET'])
def get_camera_frame():
    global last_frame
    try:
        if last_frame[request.args.get('id')] is not None:
            _, encoded_frame = cv2.imencode('.jpg', last_frame[request.args.get('id')])
            response = Response(encoded_frame.tobytes(), mimetype='image/jpeg')
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            return response
    except:
        pass


    return "No frame available"

@app.route('/send_screen', methods=['GET', 'POST'])
def send_screen():
    global screen_last_frame
    if request.method == 'POST':
        frame_data = request.data
        frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)

        if frame is not None:
            screen_last_frame[request.args.get('id')] = frame

        return Response(status=200)

@app.route('/get_screen_frame', methods=['GET'])
def get_screen_frame():
    global screen_last_frame
    try:
        if screen_last_frame[request.args.get('id')] is not None:
            _, encoded_frame = cv2.imencode('.jpg', screen_last_frame[request.args.get('id')])
            response = Response(encoded_frame.tobytes(), mimetype='image/jpeg')
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            return response
    except:
        pass

    return "No frame available"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=20015)