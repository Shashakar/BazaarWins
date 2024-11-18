import easyocr
import logging
from logging_bazaar import setup_logging

# Set up logging
logger = setup_logging(logging.DEBUG, "TextReader")

def handle_full_screenshot(path):
    try:
        # For each png in game_examples, log the detected text and confidence
        result = get_text_from_image(path)
        for detection in result:
            logger.info(f"Detected text: {detection[1]}, with confidence: {detection[2]}")
    except Exception as e:
        logger.error(f"Error in handle_full_screenshot: {e}")

def get_text_from_image(image_path):
    try:
        reader = easyocr.Reader(['en'])  # Specify the languages to use
        result = reader.readtext(image_path)
        return result
    except Exception as e:
        logger.error(f"Error in get_text_from_image: {e}")
        return []

def get_user_and_title_from_image(image_path):
    try:
        result = get_text_from_image(image_path)
        title = result[0][1]
        user = result[1][1]
        logger.info(f"Title: {title}, User: {user}")
        return title, user
    except Exception as e:
        logger.error(f"Error in get_user_and_title_from_image: {e}")
        return None, None

def get_wins_from_image(image_path):
    try:
        result = get_text_from_image(image_path)
        wins_number = result[1][1]
        wins_status = result[2][1]
        logger.info(f"Wins Number: {wins_number}, Wins Status: {wins_status}")
        return wins_number, wins_status
    except Exception as e:
        logger.error(f"Error in get_wins_from_image: {e}")
        return None, None

def get_stats_from_image(image_path):
    try:
        result = get_text_from_image(image_path)
        health = result[0][1]
        prestige = result[1][1]
        xp = result[2][1]
        income = result[3][1]
        money = result[4][1]
        #logger.debug(f"Health: {health}, Prestige: {prestige}, XP: {xp}, Income: {income}, Money: {money}")
        return health, prestige, xp, income, money
    except Exception as e:
        logger.error(f"Error in get_stats_from_image: {e}")
        return None, None, None, None, None

def get_first_text_from_image(image_path):
    try:
        result = get_text_from_image(image_path)
        text = result[0][1]
        #logger.debug(f"First Text: {text}")
        return text
    except Exception as e:
        logger.error(f"Error in get_first_text_from_image: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    example_image_path = "example_screenshot.png"
    handle_full_screenshot(example_image_path)
    get_user_and_title_from_image(example_image_path)
    get_wins_from_image(example_image_path)
    get_stats_from_image(example_image_path)
    get_first_text_from_image(example_image_path)
