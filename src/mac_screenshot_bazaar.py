import os
import logging
import Quartz.CoreGraphics as CG
from PIL import Image
from logging_bazaar import setup_logging

# Set up logging
logger = setup_logging(logging.DEBUG, "MacScreenshotHandler")

data_folder = os.path.join("..", "data")
window_title = "The Bazaar"

# Function to capture the screenshot of a specific window
def take_screenshot_of_window():
    try:
        # Get list of windows
        window_list = CG.CGWindowListCopyWindowInfo(CG.kCGWindowListOptionOnScreenOnly, CG.kCGNullWindowID)
        target_window = None

        # Find the target window by title or owner name
        for window in window_list:
            window_name = window.get('kCGWindowName', '')
            window_owner_name = window.get('kCGWindowOwnerName', '')

            # Log the details of each window for debugging purposes
            #logger.debug(f"Window in list: {window}")

            if (window_title.lower() in window_name.lower()) or (window_title.lower() in window_owner_name.lower()):
                target_window = window
                break

        # Ensure we found a window with the specified title
        if not target_window:
            logger.error(f"Window with title '{window_title}' not found.")
            return

        # Get the window bounds
        bounds = target_window['kCGWindowBounds']
        x, y, width, height = int(bounds['X']), int(bounds['Y']), int(bounds['Width']), int(bounds['Height'])

        # Capture the screenshot of the specific region
        screenshot = CG.CGWindowListCreateImage(
            CG.CGRectMake(x, y, width, height),
            CG.kCGWindowListOptionIncludingWindow, target_window['kCGWindowNumber'],
            CG.kCGWindowImageDefault
        )

        if not screenshot:
            logger.error("Failed to capture the screenshot of the specified window.")
            return

        # Convert Quartz CGImage to PIL Image
        pil_image = convert_cgimage_to_pil(screenshot)

        # Save the screenshot to a file
        screenshot_name = f"{window_title.replace(' ', '_')}_screenshot.png"
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)

        screenshot_path = os.path.join(data_folder, screenshot_name)
        pil_image.save(screenshot_path, "PNG")

        logger.info(f"Screenshot saved to: {screenshot_path}")
        return screenshot_path

    except Exception as e:
        logger.error(f"An error occurred while taking a screenshot: {e}")
        return

def convert_cgimage_to_pil(cg_image):
    """Convert a Quartz CGImageRef to a PIL Image"""
    width = CG.CGImageGetWidth(cg_image)
    height = CG.CGImageGetHeight(cg_image)
    bytes_per_row = CG.CGImageGetBytesPerRow(cg_image)
    color_space = CG.CGImageGetColorSpace(cg_image)
    data_provider = CG.CGImageGetDataProvider(cg_image)
    data = CG.CGDataProviderCopyData(data_provider)

    # Create the PIL Image from the raw data
    pil_image = Image.frombytes("RGBA", (width, height), data, "raw", "RGBA", bytes_per_row)
    return pil_image

if __name__ == "__main__":
    take_screenshot_of_window()
