import os
import logging
import sys
import time
import platform

from bazaar_api import upload_game_stats
from cloudinary_handler import upload_image_to_cloudinary
from logging_bazaar import setup_logging
from text_detection import get_user_and_title_from_image, get_wins_from_image, \
    get_first_text_from_image
from crop_images import crop_and_save_images
from watcher import is_bazaar_active, detect_wins_screen, take_full_screenshot

if getattr(sys, 'frozen', False):  # Running as a PyInstaller executable
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

templates_folder = os.path.join(base_path, 'templates')

# Use the appropriate screenshot handler depending on the platform
if platform.system() == "Windows":
    from windows_screenshot_bazaar import take_screenshot_of_window
    wins_template = os.path.join(templates_folder, "windows_wins_template.png")
else:
    from mac_screenshot_bazaar import take_screenshot_of_window
    wins_template = os.path.join(templates_folder, "mac_wins_template.png")

next_screen_template = os.path.join(templates_folder, "next_screen_template.png")

# Set up logging
logger = setup_logging(logging.DEBUG, "Main")

data_folder = os.path.join("..", "data")

items_image = os.path.join(data_folder, "_items.png")
stats_image = os.path.join(data_folder, "_stats.png")
skills_image = os.path.join(data_folder, "_skills.png")
title_username_image = os.path.join(data_folder, "_title_username.png")
wins_image = os.path.join(data_folder, "_wins.png")
health_image = os.path.join(data_folder, "_health.png")
prestige_image = os.path.join(data_folder, "_prestige.png")
xp_image = os.path.join(data_folder, "_xp.png")
income_image = os.path.join(data_folder, "_income.png")
money_image = os.path.join(data_folder, "_money.png")



default_crop_areas_percent = {
    "title_username": (0.0, 0.185, 0.0, 0.3),  # Grand Founder and Username area (Top Left)
    "wins": (0.09, 0.28, 0.26, 0.75),  # Number of Wins and Victory Type (Top Middle)
    "items": (0.28, 0.56, 0.34, 0.99),  # Item Square Images (Upper Middle Right)
    "stats": (0.56, 0.625, 0.34, 0.94),  # Stats (Center Middle Right)
    "skills": (0.625, 0.86, 0.34, 0.94)  # Skill Circular Images (Lower Bottom Right)
}

stats_top = 0.125
stats_bot = .875
stats_crop_coords = {
    "health": (stats_top, stats_bot, .120, .292),  # Coordinates for "250"
    "prestige": (stats_top, stats_bot, .369, .49),  # Coordinates for "0"
    "xp": (stats_top, stats_bot, .55, .69),  # Coordinates for "1"
    "income": (stats_top, stats_bot, .75, .86),  # Coordinates for "5"
    "money": (stats_top, stats_bot, .85, .99)  # Coordinates for "8"
}


def workflow():
    try:
        # Get Screenshot of The Bazaar window
        logger.info("Taking screenshot of 'The Bazaar' window.")
        screenshot_path = take_screenshot_of_window()
        if not screenshot_path:
            logger.error("Failed to take screenshot of 'The Bazaar' window.")
            return

        # Crop to appropriate sections
        logger.info("Cropping screenshot to relevant sections.")
        crop_and_save_images(screenshot_path, default_crop_areas_percent)

        # Get text from the screenshot
        logger.info("Extracting title and username from image.")
        title, user = get_user_and_title_from_image(title_username_image)
        logger.info(f"Title: {title}, User: {user}")

        logger.info("Extracting wins information from image.")
        wins_number, wins_status = get_wins_from_image(wins_image)
        logger.info(f"Wins: {wins_number}, Wins Status: {wins_status}")

        # Handle stats area
        logger.info("Cropping and extracting stats from image.")
        crop_and_save_images(stats_image, stats_crop_coords)
        health = get_first_text_from_image(health_image)
        logger.info(f"Health: {health}")
        prestige = get_first_text_from_image(prestige_image)
        logger.info(f"Prestige: {prestige}")
        xp = get_first_text_from_image(xp_image)
        logger.info(f"XP: {xp}")
        income = get_first_text_from_image(income_image)
        logger.info(f"Income: {income}")
        money = get_first_text_from_image(money_image)
        logger.info(f"Money: {money}")

        logger.info(f"Bazaar Run Complete. Run Data for '{title}' {user}:")
        logger.info(f"Wins: {wins_number}\nWins Status: {wins_status}")
        logger.info(
            f"Max Health: {health}\nPrestige Remaining: {prestige}\nXP: {xp}\nIncome Per Turn: {income}\nMoney Remaining: {money}")

        # Upload the items image to Cloudinary
        items_image_url = upload_image_to_cloudinary(items_image)
        if not items_image_url:
            logger.error("Failed to upload items image to Cloudinary.")
            items_image_url = "Error"

        logger.info(f"Items image uploaded to Cloudinary. URL: {items_image_url}")

        game_stats = {
            "username": user,
            "wins": wins_number,
            "victory_type": wins_status,
            "health": health,
            "prestige": prestige,
            "xp": xp,
            "income": income,
            "money": money,
            "items_image": items_image_url
        }
        upload_game_stats(game_stats)

    except Exception as e:
        logger.error(f"An error occurred during the workflow: {e}")

def looper():
    wins_screen_active = False
    non_active_count = 0
    active_count = 0
    while True:
        try:
            # Check if "The Bazaar" is the active window
            if is_bazaar_active():
                non_active_count = 0

                if active_count == 0:
                    logger.info("'The Bazaar' is active. Waiting for the WINS screen...")

                active_count += 1

                if active_count % 30 == 0:
                    active_count = 0

                # Take a full screenshot
                screenshot = take_full_screenshot()

                # Check if the WINS screen is visible
                detected, _ = detect_wins_screen(screenshot, wins_template)

                if detected and not wins_screen_active:
                    # WINS screen detected for the first time
                    logger.info("WINS screen detected. Starting main workflow...")
                    time.sleep(1.5)
                    workflow()  # Trigger the workflow to scrape and upload stats
                    wins_screen_active = True  # Set flag to prevent duplicate processing

                elif wins_screen_active:
                    # Check if the next screen is visible
                    next_screen_detected, _ = detect_wins_screen(screenshot, next_screen_template)
                    if next_screen_detected:
                        logger.info("Next screen detected. Resetting state for watching the WINS screen.")
                        wins_screen_active = False

            else:
                active_count = 0
                if non_active_count == 0:
                    logger.info("'The Bazaar' is not active. Waiting for it to become active...")

                non_active_count += 1

                if non_active_count % 30 == 0:
                    non_active_count = 0

            # Sleep for a short time to avoid excessive CPU usage
            time.sleep(1)

        except Exception as e:
            logger.error(f"An error occurred in the main loop: {e}")
            time.sleep(5)  # Pause before retrying in case of an error

if __name__ == "__main__":
    logger.info("Starting to watch for the WINS screen while 'The Bazaar' is active...")
    looper()
