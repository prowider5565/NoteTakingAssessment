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

    ACCESS_EXP_MINUTES: int
    REFRESH_EXP_DAYS: int
    ALGORITHM: str
    SECRET_KEY: str

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

    @property
    def postgres_url(self):
        return (
            f"postgresql://{self.POSTGRES_USERNAME}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}/{self.POSTGRES_NAME}"
        )

    class Config:
        env_file = ".env"


settings = Settings()
