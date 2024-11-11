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

# Template image of the WINS screen
template_path = os.path.join(".", "training_images", 'wins_template.png')

# Load the template image
template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
if template is None:
    logger.error(f"Error: Unable to load template image '{template_path}'")
    exit()

# Template dimensions
template_height, template_width = template.shape

# Function to take a screenshot of the entire screen
def take_full_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot_np = np.array(screenshot)
    screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    return screenshot_bgr

# Function to detect the WINS screen using template matching
def detect_wins_screen(screenshot, template):
    # Convert screenshot to grayscale
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Perform template matching
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Threshold for detection
    threshold = 0.8  # You may need to adjust this value
    if max_val >= threshold:
        logger.info(f"WINS screen detected with confidence {max_val:.2f}")
        return True, max_loc
    return False, None

# Function to check if "The Bazaar" is the active window
def is_bazaar_active():
    active_window = gw.getActiveWindow()
    if active_window and "The Bazaar" in active_window.title:
        return True
    return False

# Function to watch for the WINS screen when "The Bazaar" is active
def watch_for_wins_screen():
    while True:
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

# Main script entry point
if __name__ == "__main__":
    logger.info("Starting to watch for the WINS screen while 'The Bazaar' is active...")
    watch_for_wins_screen()
