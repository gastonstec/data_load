# Logging imports
import logging
import sys
from core.config import AppSettings, EnvSettings

# Setup logger
logger = logging.getLogger(AppSettings.name)
# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Configure logger by environment
if EnvSettings.debug:
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler(sys.stdout)
else:
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
# Attach the handler to the logger
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)