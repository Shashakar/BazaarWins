import logging

from bazaar_scraper import looper
from logging_bazaar import setup_logging
from src.updater import run_updater
from updater import check_for_updates

logger = setup_logging(logging.DEBUG, "ApplicationHandler")

def check_for_available_updates():
    logger.info("Checking for updates..")
    available_update = check_for_updates()
    return available_update

def start_scraper():
    logger.info("Starting the application..")
    looper()

if __name__ == "__main__":
    is_update_available = check_for_available_updates()
    if is_update_available:
        run_updater()
    else:
        start_scraper()