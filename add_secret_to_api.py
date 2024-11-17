import requests
import getpass

BASE_URL = "https://bazaar-stats-2d776b50c345.herokuapp.com"
# Constants
API_URL = "http://127.0.0.1:5000/api/secrets"  # Replace with your actual API endpoint URL


def add_secret():
    # Prompt user for the secret name
    secret_name = input("Enter the name of the secret: ")

    # Prompt user for the secret value securely (without echoing)
    secret_value = getpass.getpass("Enter the secret value: ")

    # Prepare data to send to the API
    data = {
        "name": secret_name,
        "value": secret_value
    }

    # Send POST request to the API
    try:
        response = requests.post(API_URL, json=data)

        # Check response status
        if response.status_code == 201:
            print("Secret added successfully.")
        elif response.status_code == 400:
            print(f"Error: {response.json().get('message')}")
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while trying to add the secret: {e}")


if __name__ == "__main__":
    add_secret()