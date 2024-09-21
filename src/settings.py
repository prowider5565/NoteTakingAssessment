import logging
from pydantic_settings import BaseSettings
from typing import Any, Dict


class Settings(BaseSettings):
    # API credentials
    HOST: str
    PORT: int
    DOMAIN: str

    # Postgres Database credentials
    POSTGRES_NAME: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str

    # Bot Credentials
    TOKEN: str

    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "var/app.log"

    def setup_logging(self) -> None:
        """Sets up logging configuration based on settings."""
        logging.basicConfig(
            level=self.LOG_LEVEL,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(self.LOG_FILE),
            ],
        )

    class Config:
        env_file = ".env"
