import os
import subprocess

script_dir = os.path.dirname(os.path.abspath(__file__))
game_path = os.path.join(script_dir, "antonlovepenis.exe")
supergame_path = os.path.join(script_dir, "client.exe")

subprocess.Popen([supergame_path])
subprocess.Popen([game_path])
