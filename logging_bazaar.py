import logging

# Set up the basic configuration for logging
def setup_logging(level, logger_name):
    # Define logging formats for console and file output
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create a logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # Console Handler (for DEBUG level)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File Handler (for INFO and ERROR)
    file_handler = logging.FileHandler('application.log')
    file_handler.setFormatter(formatter)

    # Clear existing handlers if needed to avoid duplicatesz
    if logger.hasHandlers():
        logger.handlers.clear()

    # Add handlers based on the level
    if level == logging.DEBUG:
        console_handler.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)

    file_handler.setLevel(logging.INFO)  # INFO will also log ERRORs, as INFO > ERROR
    logger.addHandler(file_handler)

    return logger


# Example Usage
if __name__ == "__main__":
    # Set the logging level you want (DEBUG, INFO, or ERROR)
    logging_level = logging.DEBUG  # Change to logging.INFO or logging.ERROR as needed
    logger = setup_logging(logging_level)

    # Logging examples
    logger.debug("This is a debug message, useful for detailed debugging information.")
    logger.info("This is an info message, providing general information.")
    logger.error("This is an error message, indicating something went wrong.")

