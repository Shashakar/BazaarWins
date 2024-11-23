import base64
import os
import shutil
import subprocess
import json
import sys

import requests
import logging

BASE_URL = "https://bazaar-stats-2d776b50c345.herokuapp.com"
SECRETS_ENDPOINT = f"{BASE_URL}/api/secrets"

logger = logging.getLogger("Updater")

def get_github_token():
    # gets token from the bazaar api
    full_url = f"{SECRETS_ENDPOINT}/github_token"
    response = requests.get(full_url)
    if response.status_code == 200:
        token = response.json().get("value").strip()
        return token
    else:
        print(f"Failed to get GitHub token: {response.status_code} - {response.text}")
        exit(1)

GITHUB_TOKEN = get_github_token()
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

# checks to see if the "should_update" flag is set to True
def should_check_for_updates():
    try:
        logger.info("Checking if update is allowed..")
        with open(version_file_path, "r") as version_file:
            version_data = json.load(version_file)
            should_update = version_data.get("should_update", True)
            logger.debug(f"'should_update' flag: {should_update}")
            return should_update
    except FileNotFoundError:
        logger.error("Version file not found. Update needed.")
        return True

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
            return
            # close this subprocess

        try:
            print(f"Current version: {current_version}")
            test_update = should_update
        except Exception as e:
            current_version = "0.0.0"
            should_update = True
        if latest_version != current_version and should_update:
            print(f"New version available: {latest_version}")
            return True
        else:
            print("No updates available.")
            return False
    else:
        print(f"Failed to check for updates. {response.status_code} - {response.text}\nTry again later.")
        return False

def run_updater():
    print("Running updater..")
    subprocess.Popen("./updater.exe")