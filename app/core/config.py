import logging
from dotenv import load_dotenv
from pydantic_settings import BaseSettings  # ✅ Improved import!

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Configuration settings loaded from environment variables."""

    IPSTACK_API_KEY: str  # API key for IPStack service
    BASE_URL: str  # Base URL for external API requests
    LOGGER_LEVEL: str = "INFO"  # Logging level (default: INFO)
    HOST: str = "127.0.0.1"  # Server host
    PORT: int = 8000  # Server port
    DATABASE_URL: str  # Database connection URL

    class Config:
        env_file = ".env"  # Load values from .env file
        env_file_encoding = "utf-8"


# Global settings instance used throughout the application
settings = Settings()

# Validate and set logger level
if settings.LOGGER_LEVEL.upper() not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
    settings.LOGGER_LEVEL = "INFO"
    logging.warning("Invalid LOGGER_LEVEL in .env. Defaulting to INFO.")

LOG_LEVEL = getattr(logging, settings.LOGGER_LEVEL.upper(), logging.INFO)