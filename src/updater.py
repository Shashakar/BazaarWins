import base64
import os
import shutil
import subprocess
import json
import sys

import requests


if getattr(sys, 'frozen', False):  # Running as a PyInstaller executable
    token_path = sys._MEIPASS
else:
    token_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

token_path = os.path.join(token_path, "github_token")
print(token_path)

# read base64 encoded token from file
with open(token_path, "r") as token_file:
    token = token_file.read().strip()

GITHUB_TOKEN = base64.b64decode(token).decode("utf-8")
REPO_OWNER = "Shashakar"
REPO_NAME = "BazaarWins"
version_file_path = "version.json"

# checks for the deploy_files folder
# if it exists, then grab the latest version in there
# if it exists, then look for the updater.exe file
# if it exists, then replace the updater.exe file in the root folder with the one in the deploy_files folder
def check_for_available_updater():
    if os.path.exists("deploy_files"):
        version_folders = os.listdir("deploy_files")
        if len(version_folders) > 0:
            latest_version = max(version_folders)
            updater_path = os.path.join("deploy_files", latest_version, "updater.exe")
            if os.path.exists(updater_path):
                print("Updater found.")
                print(f"Copying updater.exe to root folder..")
                shutil.copy(updater_path, "updater.exe")
            else:
                print("Updater not found.")
        else:
            print("No versions found.")
    else:
        print("No deploy_files folder found.")


def check_for_updates():
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(
        f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest",
        headers=headers
    )

    if response.status_code == 200:
        latest_release = response.json()
        latest_version = latest_release["tag_name"].strip()
        print(f"Latest version available: {latest_version}")

        # Load version data
        try:
            with open(version_file_path, "r") as version_file:
                version_data = json.load(version_file)
                current_version = version_data.get("version", "0.0.0").strip()
                should_update = version_data.get("should_update", True)
        except FileNotFoundError:
            run_updater()


        print(f"Current version: {current_version}")
        if latest_version != current_version and should_update:
            print(f"New version available: {latest_version}")
            run_updater()
        else:
            print("No updates available.")
    else:
        print(f"Failed to check for updates. {response.status_code} - {response.text}\nTry again later.")

def run_updater():
    print("Running updater..")
    #subprocess.Popen("./updater.exe")