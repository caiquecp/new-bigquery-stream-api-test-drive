import logging
import sys

from app.settings import Settings


def create_logger(settings: Settings) -> logging.Logger:
    logger = logging.getLogger("bq_stream_writer.logger")
    logger.setLevel(settings.APP_LOG_LEVEL)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(settings.APP_LOG_FORMAT))

    logger.addHandler(handler)

    return logger
