import requests
import logging

from logging_bazaar import setup_logging

#BASE_URL = "http://127.0.0.1:5000"
BASE_URL = "https://bazaar-stats-2d776b50c345.herokuapp.com"
UPLOAD_ENDPOINT = f"{BASE_URL}/api/upload"
GET_STATS_ENDPOINT = f"{BASE_URL}/api/stats"

logger = setup_logging(logging.DEBUG, "API")

def upload_game_stats(game_stats):
    try:
        print(f"Uploading to {UPLOAD_ENDPOINT}")
        response = requests.post(UPLOAD_ENDPOINT, json=game_stats)
        if response.status_code == 200:
            logger.info("Game stats uploaded successfully.")
        else:
            logger.error(f"Failed to upload game stats. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        logger.error(f"An error occurred while uploading game stats: {str(e)}")

def get_user_stats(username):
    try:
        response = requests.get(f"{GET_STATS_ENDPOINT}/{username}")
        if response.status_code == 200:
            stats = response.json()
            logger.info(f"Retrieved stats for {username}: {stats}")
            return stats
        else:
            logger.error(f"Failed to retrieve stats for {username}. Status code: {response.status_code}, Response: {response.text}")
            return None
    except Exception as e:
        logger.error(f"An error occurred while retrieving user stats: {str(e)}")
        return None

def workflow():
    try:
        # Simulated game stats (replace with actual scraped data)
        game_stats = {
            "username": "Player1",
            "wins": 10,
            "victory_type": "Gold",
            "health": 250,
            "prestige": 0,
            "xp": 1,
            "income": 5,
            "money": 8
        }

        # Upload the scraped game stats to the API
        logger.info("Uploading scraped game stats to the API...")
        upload_game_stats(game_stats)

        # Retrieve stats for a specific user to verify the upload
        # logging.info(f"Retrieving stats for user: {game_stats['username']}")
        # retrieved_stats = get_user_stats(game_stats["username"])
        # if retrieved_stats:
        #     logging.info(f"Retrieved Stats: {retrieved_stats}")

    except Exception as e:
        logging.error(f"An error occurred in the workflow: {e}")

if __name__ == "__main__":
    logger.basicConfig(level=logging.INFO)
    workflow()