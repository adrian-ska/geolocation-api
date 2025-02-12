from typing import Any
from pydantic import BaseModel, Field, field_validator, IPvAnyAddress
import tldextract


class GeoRequest(BaseModel):
    """Validates an IP address or domain name."""

    ip_or_url: str | IPvAnyAddress = Field(..., description="IP address or domain name")

    @staticmethod
    def clean_protocol(value: str) -> str:
        """Removes http, https, or ftp from the input string."""
        PROHIBITED_PROTOCOLS = ("http://", "https://", "ftp://")
        for protocol in PROHIBITED_PROTOCOLS:
            if value.startswith(protocol):
                return value[len(protocol):]  # Remove the protocol
        return value

    @field_validator("ip_or_url", mode="before")
    @classmethod
    def validate_ip_or_url(cls, value: str) -> str:
        """Ensures the value is a valid IP or domain without a protocol."""
        value = cls.clean_protocol(value)  # Remove protocol if present

        # If it's a valid IP, return it
        try:
            ip_address = IPvAnyAddress(value)
            return str(ip_address)
        except ValueError:
            # If not an IP, check if it's a valid domain
            extracted = tldextract.extract(value)
            if extracted.domain and extracted.suffix:
                return value.lower()  # Convert to lowercase

        raise ValueError(f"Invalid IP or domain: {value}")


class GeoLocationResponse(BaseModel):
    """Response schema for geolocation data."""

    id: int
    ip_or_url: str
    country: str | None = None
    region: str | None = None
    city: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class GeoLocationSerializer(BaseModel):
    """Schema for saving geolocation data in the database."""

    ip_or_url: str
    country: str | None = None
    region: str | None = None
    city: str | None = None
    latitude: float | None = None
    longitude: float | None = None