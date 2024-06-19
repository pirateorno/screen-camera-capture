import platform
import re
import uuid
from datetime import datetime

import cpuinfo
import psutil
import requests

import win32com.client
import ctypes
import os


def get_size(bytes, suffix="B"):

	factor = 1024
	for unit in ["", "K", "M", "G", "T", "P"]:
		if bytes < factor:
			return f"{bytes:.2f}{unit}{suffix}"
		bytes /= factor


def isAdmin():
	try:
		is_admin = (os.getuid() == 0)
	except AttributeError:
		is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
	return is_admin

def get_antivirus():
	# Connect to the WMI service
	objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
	swbemServices = objWMIService.ConnectServer(".", "ROOT\\SecurityCenter2")

	# Execute the WMI query to get antivirus product information
	colItems = swbemServices.ExecQuery("SELECT * FROM AntivirusProduct")

	# Check the status of each antivirus product
	for objItem in colItems:
		name = objItem.displayName
		state = objItem.productState
		state_hex = f'{state:06x}'  # Format as hex with leading zeros

		# Extract the middle two hex digits and check if enabled
		enabled_hex = state_hex[2:4]
		enabled_status = 'Enabled' if enabled_hex == '10' else 'Disabled'

		# Extract the last two hex digits for update status
		update_hex = state_hex[4:6]
		update_status = 'Up to Date' if update_hex == '00' else 'Not Up to Date'

		return name
		#print(f'State (Hex): {state_hex.upper()}')
		#print(f'Enabled Status: {enabled_status}')
		#print(f'Update Status: {update_status}\n')

def System_information():
	text = ""
	text += "=" * 20 + "System Information" + "=" * 20 + "\n"
	uname = platform.uname()
	text += f"System: {uname.system}\n"
	text += f"Release: {uname.release}\n"
	text += f"Version: {uname.version}\n"
	text += f"Machine: {uname.node}\n"
	text += f"Processor: {cpuinfo.get_cpu_info()['brand_raw']}\n"
	text += f"Ip-Address: {requests.get('https://api.ipify.org').text}\n"
	text += f"Mac-Address: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}\n"

	# Boot Time
	text += "=" * 20 + "Boot Time" + "=" * 20 + "\n"
	boot_time_timestamp = psutil.boot_time()
	bt = datetime.fromtimestamp(boot_time_timestamp)
	text += f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}\n"

	# CPU Info
	text += "=" * 20 + "CPU Info" + "=" * 20 + "\n"
	# number of cores
	text += "Physical cores:" + str(psutil.cpu_count(logical=False)) + "\n"
	text += "Total cores:" + str(psutil.cpu_count(logical=True)) + "\n"
	text += f"Total CPU Usage: {psutil.cpu_percent()}%\n"

	# Other
	text += "=" * 20 + "Other" + "=" * 20 + "\n"
	text += f"Antivirus: {get_antivirus()}\n"
	text += f"Is admin: {isAdmin()}\n"

	# Memory Information
	text += "=" * 20 + "Memory Information" + "=" * 20 + "\n"
	# get the memory details
	svmem = psutil.virtual_memory()
	text += f"Total: {get_size(svmem.total)}\n"
	text += f"Available: {get_size(svmem.available)}\n"
	text += f"Used: {get_size(svmem.used)}\n"
	text += f"Percentage: {svmem.percent}%\n"

	# Disk Information
	text += "=" * 20 + "Disk Information" + "=" * 20 + "\n"
	text += "Partitions and Usage:\n"
	# get all disk partitions
	partitions = psutil.disk_partitions()
	for partition in partitions:
		text += f"=== Device: {partition.device} ===\n"
		text += f"  Mountpoint: {partition.mountpoint}\n"
		text += f"  File system type: {partition.fstype}\n"
		try:
			partition_usage = psutil.disk_usage(partition.mountpoint)
		except PermissionError:
			continue
		text += f"  Total Size: {get_size(partition_usage.total)}\n"
		text += f"  Used: {get_size(partition_usage.used)}\n"
		text += f"  Free: {get_size(partition_usage.free)}\n"
		text += f"  Percentage: {partition_usage.percent}%\n"

	return text