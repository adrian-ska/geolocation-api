import socket
from typing import Optional, Dict, Any

from fastapi import HTTPException
from app.clients.ipstack import IPStackClient
from app.core.logger import logger
from app.schemas.geolocation import GeoRequest, GeoLocationSerializer

class GeolocationService:

    @staticmethod
    def resolve_url_to_ip(url: str) -> Optional[str]:
        """
        Converts a URL to an IP address if needed.

        :param url: The URL to resolve.
        :return: The corresponding IP address or None if resolution fails.
        """
        try:
            ip_address = socket.gethostbyname(url)
            logger.info(f"Resolved URL '{url}' to IP: {ip_address}")
            return ip_address
        except socket.gaierror:
            logger.warning(f"Could not resolve URL '{url}' to an IP address")
            return None

    @staticmethod
    def validate_geolocation_data(data: Dict[str, Any]) -> dict:
        """
        Validates geolocation data received from IPStack API.

        :param data: The geolocation data returned from IPStack.
        :return: The validated data or raises an HTTPException if invalid.
        """
        if not data or "country_name" not in data:
            logger.error(f"Invalid API response: {data}")
            raise HTTPException(status_code=400, detail="Invalid geolocation data received from API")

        logger.info(f"Validated geolocation data for country: {data['country_name']}")
        return data

    @staticmethod
    def format_geolocation_response(ip_or_url: str, data: Dict[str, Any]) -> GeoLocationSerializer:
        """
        Formats the raw geolocation data into a structured response.

        :param ip_or_url: The original IP or URL provided by the user.
        :param data: The raw geolocation data retrieved from the API.
        :return: A structured GeoLocationSerializer object.
        """
        logger.info(f"Formatting response for {ip_or_url}")
        try:
            return GeoLocationSerializer(
                ip_or_url=ip_or_url,
                country=data.get("country_name"),
                region=data.get("region_name"),
                city=data.get("city"),
                latitude=data.get("latitude"),
                longitude=data.get("longitude"),
            )
        except Exception as e:
            logger.error(f"Failed to format geolocation response: {e}")
            raise ValueError("Invalid geolocation data received.")

    async def get_geolocation(self, request: GeoRequest) -> GeoLocationSerializer:
        """
        Handles a geolocation request by resolving the input and fetching geolocation data.

        :param request: The geolocation request containing an IP or URL.
        :return: A formatted GeoLocationSerializer response.
        """
        ip_address = self.resolve_url_to_ip(request.ip_or_url) or request.ip_or_url
        data = await IPStackClient.fetch_geolocation(ip_address)

        if not data or "country_name" not in data:
            logger.error(f"API request failed for {ip_address}: {data}")
            raise HTTPException(status_code=502, detail="Geolocation API error or invalid response")

        logger.info(f"Successfully retrieved geolocation for {ip_address}")
        return self.format_geolocation_response(ip_address, data)