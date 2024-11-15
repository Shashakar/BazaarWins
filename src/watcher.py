import platform

import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
import time
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('ScreenWatcher')


# Function to load a template image and validate its type
def load_template_image(template_path):
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        logger.error(f"Error: Unable to load template image '{template_path}'")
        return None
    if not isinstance(template, np.ndarray):
        logger.error(f"Error: Loaded template is not a valid numpy array. Template path: '{template_path}'")
        return None
    return template

# Function to take a screenshot of the entire screen
def take_full_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot_np = np.array(screenshot)
    screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    return screenshot_bgr

# Function to detect the WINS screen using template matching
def detect_wins_screen(screenshot, template_path):
    template = load_template_image(template_path)
    # Ensure the template is loaded and is a numpy array
    if template is None or not isinstance(template, np.ndarray):
        logger.error(f"Template image is not loaded or is not a valid numpy array. Cannot perform template matching")
        return False, None

    try:
        # Convert screenshot to grayscale
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

        # Perform template matching
        result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Threshold for detection
        threshold = 0.8  # You may need to adjust this value
        if max_val >= threshold:
            logger.info("Still on existing WINS screen, waiting to proceed before resetting state.")
            return True, max_loc
    except Exception as e:
        logger.error(f"Error occurred during template matching: {e}")

    return False, None

# Function to check if "The Bazaar" is the active window on Windows
def is_bazaar_active():
    if platform.system() == "Windows":
        # Only perform this check on Windows
        active_window = gw.getActiveWindow()
        if active_window and "The Bazaar" in active_window.title:
            return True
        return False
    else:
        # On macOS or other platforms, return True to proceed
        return True

# Function to watch for the WINS screen when "The Bazaar" is active
def watch_for_wins_screen():
    while True:
        try:
            # Check if "The Bazaar" is the active window
            if is_bazaar_active():
                # Take a screenshot
                screenshot = take_full_screenshot()

                # Check if the WINS screen is visible
                detected, location = detect_wins_screen(screenshot, template)
                if detected:
                    # Take a screenshot and save it
                    screenshot_path = f'wins_screen_{int(time.time())}.png'
                    cv2.imwrite(screenshot_path, screenshot)
                    logger.info(f"WINS screen detected and saved to: {screenshot_path}")

                    # Break or continue watching as needed
                    break
            else:
                logger.info("The Bazaar is not active. Waiting for it to become active...")

            # Sleep for a short time to avoid excessive CPU usage
            time.sleep(1)

        except Exception as e:
            logger.error(f"An error occurred in the main loop: {e}")
            time.sleep(5)  # Pause before retrying in case of an error

# Main script entry point
if __name__ == "__main__":

    # Template image of the WINS screen
    template_path = os.path.join("..", "training_images", 'wins_template.png')

    # Load the template image with error checking
    template = load_template_image(template_path)

    # Template dimensions (only if template is loaded)
    if template is not None:
        template_height, template_width = template.shape

    if template is None:
        logger.error("Template image could not be loaded. Exiting program.")
    else:
        logger.info("Starting to watch for the WINS screen while 'The Bazaar' is active...")
        watch_for_wins_screen()