import logging

# Define a consistent log format with timestamp, log level, module, and message
LOG_FORMAT = "%(asctime)s - [%(levelname)s] - %(module)s - %(message)s"

# Configure the logger with the specified format and default log level (INFO)
logging.basicConfig(
    format=LOG_FORMAT,
    level=logging.INFO,  # Change to DEBUG, WARNING, ERROR as needed
)

# Create a logger instance for the application
logger = logging.getLogger("geolocation_app")