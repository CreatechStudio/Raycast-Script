#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Fluffy Launcher
# @raycast.mode silent
# @raycast.packageName fluffy-launcher

# Optional parameters:
# @raycast.icon images/fluffy-icon.png
# @raycast.argument1 {"type": "text", "placeholder": "install/start/stop/update/uninstall", "optional": false}

# Documentation:
# @raycast.description Usage: fluffy <install/start/stop/update/uninstall>

import importlib
import pip
depends = [
    ('psutil', 'psutil'),
    ('requests', 'requests')
]
for pack_name, imp_name in depends:
    try:
        importlib.import_module(imp_name)
    except:
        pip.main(['install', pack_name])

import sys

args = sys.argv[1:]

import os
import subprocess
import signal
import psutil
import requests

FLUFFY_VERSION_FILE = 'fluffy/VERSION'
FLUFFY_PID_FILE = 'fluffy/fluffy.pid'

def get_latest_version():
    try:
        response = requests.get('https://api.github.com/repos/iewnfod/fluffy/releases/latest')
        if response.status_code == 200:
            latest_version = response.json()['tag_name']
            return latest_version
    except Exception as e:
        print(f"Error fetching latest version: {e}")
    return None

def save_version_to_file(version):
    try:
        with open(FLUFFY_VERSION_FILE, 'w') as file:
            file.write(version)
    except Exception as e:
        print(f"Error saving version to file: {e}")

def read_version_from_file():
    try:
        with open(FLUFFY_VERSION_FILE, 'r') as file:
            return file.read().strip()
    except Exception as e:
        print(f"Error reading version from file: {e}")
    return None

def download_fluffy():
    folder_name = "fluffy"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    latest_version = get_latest_version()
    save_version_to_file(latest_version)
    os.system('wget -O fluffy/fluffy https://github.com/iewnfod/fluffy/releases/latest/download/fluffy')

    shell = os.getenv('SHELL')

    if shell.endswith('bash'):
        os.system(f'echo \'\' >> ~/.bashrc')
        os.system(f'echo \'#Fluffy in Raycast Shell Script\' >> ~/.bashrc')
        os.system(f'echo \'export PATH="$PATH:{os.getcwd()}/fluffy"\' >> ~/.bashrc')
    elif shell.endswith('zsh'):
        os.system(f'echo \'\' >> ~/.zshrc')
        os.system(f'echo \'#Fluffy in Raycast Shell Script\' >> ~/.zshrc')
        os.system(f'echo \'export PATH="$PATH:{os.getcwd()}/fluffy"\' >> ~/.zshrc')
    elif 'fish' in shell:
        os.system(f'echo \'\' >> ~/.config/fish/config.fish')
        os.system(f'echo \'#Fluffy in Raycast Shell Script\' >> ~/.config/fish/config.fish')
        os.system(f'echo \'set -gx PATH $PATH {os.getcwd()}/fluffy\' >> ~/.config/fish/config.fish')
    else:
        print("Shell not supported.")

    os.system('chmod +x fluffy/fluffy')

def run_fluffy_background():
    for proc in psutil.process_iter(['name']):
        if 'fluffy' in proc.info['name']:
            print("Fluffy process already running! 🚀")
            return

    process = subprocess.Popen(['./fluffy/fluffy'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    with open(FLUFFY_PID_FILE, 'w') as pid_file:
        pid_file.write(str(process.pid))

    print("🚀 Fluffy is running in the background!")

def kill_process():
    if os.path.exists(FLUFFY_PID_FILE):

        with open(FLUFFY_PID_FILE, 'r') as pid_file:
            pid = int(pid_file.read().strip())

        os.kill(pid, signal.SIGTERM)
        os.remove(FLUFFY_PID_FILE)
        print("🛑 Fluffy process terminated.")
    else:
        print("Fluffy process is not running.")

def update_fluffy():
    latest_version = get_latest_version()
    if latest_version:
        saved_version = read_version_from_file()
        if latest_version != saved_version:
            os.system(f'wget -O fluffy/fluffy https://github.com/iewnfod/fluffy/releases/latest/download/fluffy')
        else:
            print("🤔 Fluffy is already up to date.")

def uninstall_fluffy():
    if os.path.exists("fluffy"):
        subprocess.run(["rm", "-rf", "fluffy"])

    app_support_path = os.path.expanduser("~/Library/Application Support/com.iewnfod.fluffy")
    if os.path.exists(app_support_path):
        subprocess.run(["rm", "-rf", app_support_path])

    print("🗑 Fluffy has been uninstalled.")


def main():
    args = sys.argv[1:]
    if args and args[0] == 'install':
        download_fluffy()
    elif args and args[0] == 'start':
        run_fluffy_background()
    elif args and args[0] == 'stop':
        kill_process()
    elif args and args[0] == "update":
            update_fluffy()
    elif args and args[0] == "uninstall":
            uninstall_fluffy()
    else:
        print("Invalid arguments.")

if __name__ == "__main__":
    main()
