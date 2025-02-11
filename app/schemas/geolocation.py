from typing import Any
from pydantic import BaseModel, Field, field_validator, IPvAnyAddress
import tldextract


class GeoRequest(BaseModel):
    """
    Schema for validating an IP address or domain name.
    Ensures that the input is either a valid IP or a domain without a protocol.
    """
    ip_or_url: str | IPvAnyAddress = Field(..., description="IP address or domain name")

    @staticmethod
    def clean_protocol(value: str) -> str:
        """
        Removes protocol prefixes (http, https, ftp) from the input string.
        """
        PROHIBITED_PROTOCOLS = ("http://", "https://", "ftp://")
        for protocol in PROHIBITED_PROTOCOLS:
            if value.startswith(protocol):
                return value[len(protocol):]  # Remove the protocol part
        return value

    @field_validator("ip_or_url", mode="before")
    @classmethod
    def validate_ip_or_url(cls, value: str) -> str:
        """
        Validates the provided IP or domain name.
        - Removes protocols if present.
        - Accepts valid IPv4/IPv6 addresses.
        - Ensures the domain contains at least a valid root domain and suffix.
        """
        value = cls.clean_protocol(value)  # Remove protocol if exists

        # If the value is a valid IP, return it
        try:
            ip_address = IPvAnyAddress(value)
            return str(ip_address)
        except ValueError:
            # If not an IP, validate domain name
            extracted = tldextract.extract(value)
            if extracted.domain and extracted.suffix:
                return value.lower()  # Normalize to lowercase

        raise ValueError(f"Invalid input format: {value}")


class GeoLocationResponse(BaseModel):
    """Schema for returning geolocation data."""
    id: int
    ip_or_url: str
    country: str | None = None
    region: str | None = None
    city: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class GeoLocationSerializer(BaseModel):
    """Schema for serializing geolocation data before saving to the database."""
    ip_or_url: str
    country: str | None = None
    region: str | None = None
    city: str | None = None
    latitude: float | None = None
    longitude: float | None = None