from .settings import Settings


settings = Settings()
settings.setup_logging()

# this can be used anywhere so that we provide base logging accross the code
logger = logging.getLogger(__name__)
logger.info("Logging is successfully configured!")
