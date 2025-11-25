"""

# Example usage:
from src.core.logger import Logger
log = Logger.setup()
log.info("System startup complete.")

"""


import logging
import sys
from datetime import datetime

class Logger:
    @staticmethod
    def setup_logger(name: str = "casper_home", level=logging.INFO):
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Avoid duplicate handlers when re-initializing
        if logger.handlers:
            return logger

        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        logger.info(f"Logger initialized at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return logger
    
    # TODO: create functions for log.info() log.warning(), log.error() etc


