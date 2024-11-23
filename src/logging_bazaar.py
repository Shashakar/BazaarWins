import logging

# Set up the basic configuration for logging
def setup_logging(level, logger_name):
    # Define logging formats for console and file output
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create or get the logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # Avoid adding handlers if already configured
    if not logger.handlers:
        # Console Handler (for DEBUG level)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        if level == logging.DEBUG:
            console_handler.setLevel(logging.DEBUG)
            logger.addHandler(console_handler)

        # File Handler (for INFO and ERROR)
        file_handler = logging.FileHandler('./application.log')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)  # INFO will also log ERRORs, as INFO > ERROR
        logger.addHandler(file_handler)

    return logger

# Example Usage
if __name__ == "__main__":
    # Set the logging level you want (DEBUG, INFO, or ERROR)
    logging_level = logging.DEBUG  # Change to logging.INFO or logging.ERROR as needed
    logger = setup_logging(logging_level, "Main")

    # Logging examples
    logger.debug("This is a debug message, useful for detailed debugging information.")
    logger.info("This is an info message, providing general information.")
    logger.error("This is an error message, indicating something went wrong.")
