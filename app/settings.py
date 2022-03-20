import logging

from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_LOG_LEVEL: int = logging.ERROR
    APP_LOG_FORMAT: str = "[%(thread)d][%(asctime)s] %(levelname)s: %(message)s"
    BQ_PROJECT_ID: str
    BQ_DATASET_ID: str
    BQ_TABLE_ID: str
