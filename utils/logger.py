"""
The logger module supports different log levels:

logger.debug("Debug message")
logger.info("Informational message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
"""
import logging
import os
import config.constants as constants

logger = logging.getLogger('aws_rds_configuration_options')

# Define a function to initialize the logger pickup the log file name and location from constants.py
def initialize_logger():
    logger.setLevel(logging.DEBUG)

    # Check if log directory exists, if not create it
    if not os.path.exists(constants.log_dir):
        try:
            os.makedirs(constants.log_dir)
        except Exception as e:
            print(f"Could not create log directory: {e}")
            return

    # Create the file handler
    log_file = os.path.join(constants.log_dir, constants.log_filename)
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)

    # Format the log messages timestamp, log level and message
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Add formatter to file handler
    fh.setFormatter(formatter)

    # Add file handler to logger
    logger.addHandler(fh)

    # Report the log file location to stdout so the user can find it
    print(f"INFO: Log file location: {log_file}")

# Initialize the logger so execution data is written to the log file
initialize_logger()
