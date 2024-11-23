import logging
import sys
import threading
import time

from bazaar_scraper import looper
from logging_bazaar import setup_logging
from src.updater import run_updater, should_check_for_updates
from src.windowstray import start_tray_icon
from updater import check_for_updates

logger = setup_logging(logging.DEBUG, "ApplicationHandler")

def check_for_available_updates():
    if not getattr(sys, 'frozen', False):  # If running as a python script
        return False
    if should_check_for_updates():
        logger.info("Checking for updates..")
        available_update = check_for_updates()
        return available_update

def start_scraper():
    logger.info("Starting the application..")
    looper()

def start_main_thread():
    is_update_available = check_for_available_updates()
    if is_update_available:
       run_updater()
    else:
        start_scraper()

def spawn_main_thread():
    main_thread = threading.Thread(target=start_main_thread, daemon=True)
    main_thread.start()

def spawn_tray_thread():
    tray_thread = threading.Thread(target=start_tray_icon, daemon=True)
    tray_thread.start()


if __name__ == "__main__":
    spawn_tray_thread()
    spawn_main_thread()

    while True:
        time.sleep(1)