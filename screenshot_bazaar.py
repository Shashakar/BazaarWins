import os
import time
import pygetwindow as gw
import pyautogui
import logging
from logging_bazaar import setup_logging

# Set up logging
logger = setup_logging(logging.DEBUG, "ScreenshotHandler")

# Example usage
window_title = "The Bazaar"  # Replace with the title or part of the title of the window
data_folder = os.path.join(".", "data")

# Function to take a screenshot of a specific window and determine if it's windowed or maximized
def take_screenshot_of_window():
    try:
        # Get the window by title
        window = None
        for w in gw.getAllWindows():
            if window_title.lower() in w.title.lower():
                window = w
                break

        # Ensure we found a window with the specified title
        if window is None:
            logger.error(f"Window with title '{window_title}' not found.")
            return

        # Get window's bounding box coordinates
        left, top, right, bottom = window.left, window.top, window.right, window.bottom

        # Get screen dimensions
        screen_width, screen_height = pyautogui.size()

        # Ensure the window is in the foreground
        window.activate()
        time.sleep(1)

        # Determine if the window is maximized or windowed
        if window.isMaximized or (right - left == screen_width and bottom - top == screen_height):
            logger.info(f"Window '{window_title}' is maximized/fullscreen.")
            # Take a screenshot of the full window
            screenshot = pyautogui.screenshot(region=(left, top, right - left, bottom - top))
        else:
            logger.info(f"Window '{window_title}' is in windowed mode.")
            # If the window is in windowed mode, adjust for the title bar
            title_bar_height = 30  # Adjust this value based on your system
            adjusted_top = top + title_bar_height
            # Take a screenshot excluding the title bar
            screenshot = pyautogui.screenshot(region=(left, adjusted_top, right - left, bottom - adjusted_top))

        screenshot_name = f"{window_title.replace(' ', '_')}_screenshot.png"
        # Save the screenshot to a file
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)

        screenshot_path = os.path.join(data_folder, screenshot_name)
        screenshot.save(screenshot_path)

        logger.info(f"Screenshot saved to: {screenshot_path}")
        return screenshot_path
    except Exception as e:
        logger.error(f"An error occurred while taking a screenshot: {e}")
        return

if __name__ == "__main__":
    take_screenshot_of_window()
