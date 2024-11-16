import requests
import os

# GitHub API and credentials
def get_github_token():
    return "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"

def get_version():
    try:
        with open("version.txt", "r") as version_file:
            return version_file.read().strip()
    except FileNotFoundError:
        print("Error: Version file 'version.txt' not found.")
        exit(1)

def get_repo_name():
    return "BazaarWins"

def get_repo_owner():
    return "Shashakar"

def create_release(version, token, owner, name):
    RELEASE_NAME = f"Version {version}"  # Human-readable name of the release
    RELEASE_DESCRIPTION = f"Release version {version}."  # Description for the release

    # API setup
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    """Create a new release on GitHub."""
    release_data = {
        "tag_name": version,
        "name": RELEASE_NAME,
        "body": RELEASE_DESCRIPTION,
        "draft": False,
        "prerelease": False
    }
    url = f"https://api.github.com/repos/{owner}/{name}/releases"
    print(f"URL for release: {url}")
    response = requests.post(url=url,
        headers=headers,
        json=release_data
    )

    if response.status_code == 201:
        release = response.json()
        print(f"Release created: {release['html_url']}")
        return release["upload_url"].replace("{?name,label}", "?name=")
    else:
        print(f"Failed to create release: {response.status_code} - {response.text}")
        return None

def upload_files_to_release(upload_url, version, token):
    FILES_DIR = f"./deploy_files/{version}"  # Path to the directory containing files to upload
    """Upload files to the release created."""
    for filename in os.listdir(FILES_DIR):
        filepath = os.path.join(FILES_DIR, filename)
        if os.path.isfile(filepath):
            with open(filepath, "rb") as f:
                file_headers = {
                    "Authorization": f"token {token}",
                    "Content-Type": "application/zip"  # Adjust the content type if necessary
                }
                print(f"Uploading {filename}...")
                upload_response = requests.post(
                    f"{upload_url}{filename}",
                    headers=file_headers,
                    data=f
                )
                if upload_response.status_code == 201:
                    print(f"Uploaded {filename} successfully.")
                else:
                    print(f"Failed to upload {filename}: {upload_response.status_code} - {upload_response.content}")

def main():
    GITHUB_TOKEN = get_github_token()
    VERSION = get_version()
    REPO_NAME = get_repo_name()
    REPO_OWNER = get_repo_owner()

    # Step 1: Create the release
    upload_url = create_release(VERSION, GITHUB_TOKEN, REPO_OWNER, REPO_NAME)
    if upload_url:
        # Step 2: Upload files to the release
        upload_files_to_release(upload_url, VERSION, GITHUB_TOKEN)

if __name__ == "__main__":
    main()
