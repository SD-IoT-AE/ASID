"""
ASID Logging Utility
--------------------
Provides colored, timestamped logs for ASID components.
"""

import logging, sys

def setup_logger(name, log_file=None, level=logging.INFO):
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', "%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    if log_file:
        fh = logging.FileHandler(log_file)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger

# Example usage:
# logger = setup_logger("asid", "logs/asid.log")
# logger.info("System started successfully.")
