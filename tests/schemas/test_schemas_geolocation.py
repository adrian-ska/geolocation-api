import pytest
from app.schemas.geolocation import GeoRequest


@pytest.mark.parametrize(
    "valid_value, expected",
    [
        ("8.8.8.8", "8.8.8.8"),  # Valid IPv4 address
        ("192.168.1.1", "192.168.1.1"),  # Valid private IPv4 address
        ("example.com", "example.com"),  # Valid domain
        ("www.google.com", "www.google.com"),  # Valid subdomain
        ("sub.domain.co.uk", "sub.domain.co.uk"),  # Valid multi-level domain
        ("http://google.com", "google.com"),  # Protocol should be removed
        ("ftp://example.com", "example.com"),  # Protocol should be removed
    ],
)
def test_valid_ip_or_url(valid_value, expected):
    """Test valid IP addresses and domain names"""
    instance = GeoRequest(ip_or_url=valid_value)
    assert instance.ip_or_url == expected


@pytest.mark.parametrize(
    "invalid_value",
    [
        "999.999.999.999",  # IP address out of valid range
        "256.256.256.256",  # IP segments exceed the valid limit
        "invalid_url",  # Invalid domain name format
        "just_random_text",  # Neither an IP nor a valid domain
        " "                 # empty url
    ],
)
def test_invalid_ip_or_url(invalid_value):
    """Test invalid IP addresses and domain names"""
    with pytest.raises(ValueError):  # ✅ Ensuring validation fails for incorrect inputs
        GeoRequest(ip_or_url=invalid_value)
