import logging

from app.logger import create_logger
from app.settings import Settings

settings = Settings()
logger = create_logger(settings)
