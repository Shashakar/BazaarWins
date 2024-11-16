import logging

from bazaar_scraper import looper
from logging_bazaar import setup_logging
from updater import check_for_updates

logger = setup_logging(logging.DEBUG, "ApplicationHandler")

def handle_updates():
    logger.info("Checking for updates..")
    check_for_updates()

def start_scraper():
    logger.info("Starting the application..")
    looper()

if __name__ == "__main__":
    handle_updates()
    start_scraper()