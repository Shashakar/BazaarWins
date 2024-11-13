import logging
import platform
import threading
from bazaar_scraper import workflow
import macmenubar
import windowstray
from logging_bazaar import setup_logging

logger = setup_logging(logging.DEBUG, "ApplicationHandler")

# Thread-safe wrapper for the workflow
def start_scraper():
    scraper_thread = threading.Thread(target=workflow, daemon=True)
    scraper_thread.start()

if __name__ == "__main__":
    if platform.system() == "Windows":
        logger.info("Starting Windows Tray Icon.")
        tray_thread = threading.Thread(target=start_windows_tray_icon, daemon=True)
        tray_thread.start()
        tray_thread.join()
    elif platform.system() == "Darwin":
        logger.info("Starting macOS Menu Bar Icon.")
        start_mac_menu_bar()