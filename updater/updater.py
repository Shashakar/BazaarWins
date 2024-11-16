import base64
import json
import os
import shutil
import subprocess
import zipfile
from datetime import datetime, timedelta
import requests

# Paths
version_file_path = "version.json"
output_folder = "deploy_files"

# GitHub API and credentials
token = "Z2l0aHViX3BhdF8xMUFHTUlSR1EwYU1SVEloVVpMZUFvX1Fvc1g4Rm53Q0w0YkNVdDFMNmtIZW1ubUoxYVBnMml3dkhoSjJWcGZXUThBQVZCTUxHSUdMVEtzVGI1"  # Replace with your GitHub personal access token

GITHUB_TOKEN = base64.b64decode(token).decode("utf-8")
REPO_OWNER = "Shashakar"  # Replace with your GitHub username or organization name
REPO_NAME = "BazaarWins"  # Replace with your GitHub repository name

# Step 1: Check for Updates

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
                last_check = datetime.strptime(version_data.get("last_check", "1970-01-01"), "%Y-%m-%d")
                should_update = version_data.get("should_update", True)
        except FileNotFoundError:
            print("Version file not found. Creating a new one...")
            version_data = {
                "version": "0.0.0",
                "last_update": "1970-01-01",
                "last_check": "1970-01-01",
                "should_update": True
            }
            current_version = "0.0.0"
            should_update = True

        # Update last check date
        version_data["last_check"] = datetime.now().strftime("%Y-%m-%d")

        # Check if the update should proceed based on previous attempts
        if not should_update:
            last_attempt_date = datetime.strptime(version_data.get("last_update", "1970-01-01"), "%Y-%m-%d")
            if datetime.now() - last_attempt_date > timedelta(days=1):
                version_data["should_update"] = True

        if latest_version > current_version and version_data["should_update"]:
            print("A new version is available. Downloading...")
            # Find the correct asset to download (e.g., bazaar_scraper.zip)
            asset = next((a for a in latest_release["assets"] if a["name"].endswith(".zip")), None)
            if asset:
                download_url = asset["url"]
                download_latest_version(download_url, latest_version, version_data)
            else:
                print(f"No suitable asset found for version {latest_version}")
        else:
            print("You are already using the latest version.")

        # Save the updated version data
        with open(version_file_path, "w") as version_file:
            json.dump(version_data, version_file, indent=4)
    else:
        print(f"Failed to check for updates: {response.status_code} - {response.text}")


# Step 2: Download Latest Version

def download_latest_version(download_url, latest_version, version_data):
    print(f"Downloading the latest version from {download_url}")
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/octet-stream"
    }
    response = requests.get(download_url, headers=headers, stream=True)
    if response.status_code == 200:
        latest_version_zip_path = os.path.join(output_folder, latest_version, f"{REPO_NAME}.zip")
        os.makedirs(os.path.dirname(latest_version_zip_path), exist_ok=True)
        with open(latest_version_zip_path, "wb") as f:
            shutil.copyfileobj(response.raw, f)
        print(f"Downloaded the latest version to {latest_version_zip_path}")
        # Extract the zip file
        extract_zip_file(latest_version_zip_path, latest_version, version_data)
    else:
        print(f"Failed to download the latest version: {response.status_code} - {response.text}")
        version_data["should_update"] = False
        with open(version_file_path, "w") as version_file:
            json.dump(version_data, version_file, indent=4)


# Step 3: Extract Zip File

def extract_zip_file(zip_path, latest_version, version_data):
    extract_path = os.path.join(output_folder, latest_version)
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        print(f"Extracted zip file to {extract_path}")
        # Replace the current executable with the new one (optional)
        new_executable_path = os.path.join(extract_path, f"{REPO_NAME}.exe")
        replace_current_executable(new_executable_path, version_data, latest_version)
    except zipfile.BadZipFile:
        print("Failed to extract zip file. The file may be corrupted.")
        version_data["should_update"] = False
        with open(version_file_path, "w") as version_file:
            json.dump(version_data, version_file, indent=4)


# Step 4: Replace Current Executable

def replace_current_executable(new_executable_path, version_data, latest_version):
    current_executable_path = os.path.join(os.getcwd(), f"{REPO_NAME}.exe")
    backup_path = current_executable_path + ".backup"

    # Backup current executable
    if os.path.exists(current_executable_path):
        print(f"Backing up current executable to {backup_path}")
        shutil.move(current_executable_path, backup_path)

    # Replace with new executable
    print(f"Replacing current executable with {new_executable_path}")
    shutil.move(new_executable_path, current_executable_path)

    # Update version data
    version_data["version"] = latest_version
    version_data["last_update"] = datetime.now().strftime("%Y-%m-%d")
    version_data["should_update"] = True
    with open(version_file_path, "w") as version_file:
        json.dump(version_data, version_file, indent=4)

    print("Update complete. Relaunching the application...")
    relaunch_application(current_executable_path)


# Step 5: Relaunch Application

def relaunch_application(executable_path):
    try:
        subprocess.Popen([executable_path])
        print("Application relaunched.")
    except Exception as e:
        print(f"Failed to relaunch the application: {e}")


if __name__ == "__main__":
    print("Checking for updates...")
    check_for_updates()
    print("Update check complete.")

    current_executable_path = os.path.join(os.getcwd(), f"{REPO_NAME}.exe")
    print(f"Launching the application: {current_executable_path}")

    try:
        subprocess.Popen([current_executable_path])
    except Exception as e:
        print(f"Failed to launch the application: {e}")
