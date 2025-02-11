import logging
from app.core.config import LOG_LEVEL

LOG_FORMAT = "%(asctime)s - [%(levelname)s] - %(module)s - %(message)s"

logging.basicConfig(
    format=LOG_FORMAT,
    level=LOG_LEVEL,
)

logger = logging.getLogger("geolocation_app")