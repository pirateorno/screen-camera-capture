import platform
import re
import uuid
from datetime import datetime

import cpuinfo
import psutil
import requests


#####     GET ALL PC INFORMATION     #####

def get_size(bytes, suffix="B"):

	factor = 1024
	for unit in ["", "K", "M", "G", "T", "P"]:
		if bytes < factor:
			return f"{bytes:.2f}{unit}{suffix}"
		bytes /= factor

def System_information():
	text = ""
	text += "=" * 20 + "System Information" + "=" * 20 + "\n"
	uname = platform.uname()
	text += f"System: {uname.system}\n"
	text += f"Node Name: {uname.node}\n"
	text += f"Release: {uname.release}\n"
	text += f"Version: {uname.version}\n"
	text += f"Machine: {uname.machine}\n"
	text += f"Processor: {uname.processor}\n"
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