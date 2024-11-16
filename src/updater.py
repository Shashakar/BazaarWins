import subprocess
import json

import requests

GITHUB_TOKEN = "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"
REPO_OWNER = "Shashakar"
REPO_NAME = "BazaarWins"
version_file_path = "version.json"

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
    subprocess.Popen("./updater.exe")