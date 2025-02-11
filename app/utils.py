import socket
from app.core.logger import logger


def resolve_url_to_ip(ip_or_url: str) -> str:
    """Resolves a URL to an IP address, if necessary."""
    try:
        if not ip_or_url.replace('.', '').isdigit():  # Check if it's not an IP
            logger.info(f"Resolving URL to IP: {ip_or_url}")
            return socket.gethostbyname(ip_or_url)
        return ip_or_url  # Already an IP
    except socket.gaierror:
        logger.warning(f"Unable to resolve URL: {ip_or_url}")
        return ""
