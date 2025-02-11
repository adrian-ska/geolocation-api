import httpx
from typing import Dict, Any, Optional

from app.core.config import settings
from app.core.logger import logger
from app.utils import resolve_url_to_ip


class IPStackClient:
    """Handles communication with the IPStack API."""

    @staticmethod
    def resolve_ip(ip_or_url: str) -> Optional[str]:
        """
        Converts a URL to an IP address if necessary.
        Returns the IP address as a string or None if the input is invalid.
        """
        ip_address = resolve_url_to_ip(ip_or_url)
        if not ip_address:
            logger.warning(f"Invalid IP or URL provided: {ip_or_url}")
            return None
        logger.info(f"Resolved '{ip_or_url}' to IP: {ip_address}")
        return ip_address

    @staticmethod
    async def fetch_geolocation(ip: str) -> Dict[str, Any]:
        """
        Fetches geolocation data for a given IP address from the IPStack API.
        Returns a dictionary containing geolocation details or an empty dictionary in case of an error.
        """
        url = f"{settings.BASE_URL}/{ip}?access_key={settings.IPSTACK_API_KEY}"
        logger.info(f"Requesting geolocation data for IP: {ip}")

        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()

                if "error" in data:
                    logger.error(f"API error {data['error']['code']}: {data['error']['info']}")
                    return {}

                logger.info(f"Geolocation data retrieved successfully for {ip}")
                return data

        except httpx.HTTPStatusError as e:
            logger.error(f"API request failed with status {e.response.status_code}: {e.response.text}")
            return {}

        except httpx.RequestError as e:
            logger.error(f"Network error while connecting to IPStack: {e}")
            return {}

    @staticmethod
    async def fetch_geolocation_data(ip_or_url: str) -> Dict[str, Any]:
        """
        Resolves an IP or URL and retrieves its geolocation data.
        Returns geolocation information as a dictionary or an empty dictionary if the input is invalid.
        """
        logger.info(f"Processing geolocation request for: {ip_or_url}")

        ip_address = IPStackClient.resolve_ip(ip_or_url)
        if not ip_address:
            return {}

        return await IPStackClient.fetch_geolocation(ip_address)