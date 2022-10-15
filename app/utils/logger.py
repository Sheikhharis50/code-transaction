import logging
from logging import config

from config import LOGGING

# Run once at startup
config.dictConfig(LOGGING)

# Initialize logger:
logger = logging.getLogger(__name__)
