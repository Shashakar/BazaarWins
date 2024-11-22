import json
import os
import shutil
import subprocess
import zipfile

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from github_api import get_repo_owner, get_repo_name, create_release, get_github_token

# Paths
version_file_path = "version.json"
output_folder = "deploy_files"
spec_file_path = "./src/bazaar_scraper.spec"
updater_spec_file_path = "./updater/updater.spec"
dist_folder = "dist"
REPO_NAME = get_repo_name()
REPO_OWNER = get_repo_owner()

DESCRIPTION = input("What is going into this release?\n")
# Step 1: Run PyInstaller
# Bazaar Wins
try:
    print(f"Running PyInstaller with spec file: {spec_file_path}")
    subprocess.run(["pyinstaller", spec_file_path], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error running PyInstaller: {e}")
    exit(1)

# Updater
try:
    print(f"Running PyInstaller with spec file: {updater_spec_file_path}")
    subprocess.run(["pyinstaller", updater_spec_file_path], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error running PyInstaller: {e}")
    exit(1)

# Step 2: Read Version Number
try:

    with open(version_file_path, "r") as version_file:
        version_data = json.load(version_file)
        version = version_data.get("version").strip()
        print(f"Packaging version: {version}")
except FileNotFoundError:
    print(f"Error: Version file '{version_file_path}' not found.")
    exit(1)

# Step 3: Create Version Folder
version_folder_path = os.path.join(output_folder, version)
if not os.path.exists(version_folder_path):
    print(f"Creating version folder: {version_folder_path}")
    os.makedirs(version_folder_path)

# Step 4: Move Dist Folder Contents
if not os.path.exists(dist_folder):
    print(f"Error: Dist folder '{dist_folder}' not found. Did PyInstaller run successfully?")
    exit(1)

print(f"Moving files from '{dist_folder}' to 'BazaarWins.zip'")
zip_filename = os.path.join(dist_folder, "BazaarWins.zip")
with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED, allowZip64=True) as zipf:
    for root, _, files in os.walk(dist_folder):
        for file in files:
            if file == "BazaarWins.zip":
                continue
            print(f"Adding {file} to BazaarWins.zip")
            file_path = os.path.join(root, file)
            zipf.write(file_path, os.path.relpath(file_path, dist_folder))


# Move files from dist to the version folder
for item in os.listdir(dist_folder):
    if item != "BazaarWins.zip":
        continue
    source_item = os.path.join(dist_folder, item)
    dest_item = os.path.join(version_folder_path, item)
    print(f"Moving {source_item} to {dest_item}")
    if os.path.isdir(source_item):
        shutil.copytree(source_item, dest_item, dirs_exist_ok=True)
    else:
        shutil.copy2(source_item, dest_item)

print(f"Packaging complete. Files moved to '{version_folder_path}'")

# Step 6: Create Release
upload_url = create_release(version, REPO_OWNER, REPO_NAME, DESCRIPTION)
if upload_url is None:
    print("Release version may already exists, or failed to be created.")
    upload_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/tags/{version}"
    print(f"Using existing release URL: {upload_url}")

def upload_files_to_release(upload_url):
    """Upload files to the release created."""
    session = requests.Session()
    retry = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)

    for filename in os.listdir(version_folder_path):
        filepath = os.path.join(version_folder_path, filename)
        if os.path.isfile(filepath):
            with open(filepath, "rb") as f:
                file_headers = {
                    "Authorization": f"token {get_github_token()}",
                    "Content-Type": "application/zip"  # Adjust the content type if necessary
                }
                try:
                    print(f"Uploading {filename}...")
                    upload_response = session.post(
                        f"{upload_url}{filename}",
                        headers=file_headers,
                        data=f,
                        timeout=300  # Increase timeout to 5 minutes
                    )
                    if upload_response.status_code == 201:
                        print(f"Uploaded {filename} successfully.")
                    else:
                        print(f"Failed to upload {filename}: {upload_response.status_code} - {upload_response.content}")
                except requests.exceptions.RequestException as e:
                    print(f"Error uploading {filename}: {e}")

# Step 8: Get the upload URL of the existing release
release_tag = version
headers = {
    "Authorization": f"token {get_github_token()}",
    "Accept": "application/vnd.github.v3+json"
}
response = requests.get(
    f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/tags/{release_tag}",
    headers=headers
)

if response.status_code == 200:
    release = response.json()
    upload_url = release["upload_url"].replace("{?name,label}", "?name=")
    upload_files_to_release(upload_url)
else:
    print(f"Failed to get release: {response.status_code} - {response.text}")
    exit(1)

print("Deployment complete.")