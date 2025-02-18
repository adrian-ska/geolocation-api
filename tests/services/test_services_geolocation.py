import pytest
from app.services.geolocation import GeolocationService, GeoRequest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
@patch("app.clients.ipstack.IPStackClient.fetch_geolocation", new_callable=AsyncMock)
async def test_get_geolocation(mock_fetch):
    mock_fetch.return_value = {
        "country_name": "United States",
        "region_name": "California",
        "city": "Mountain View",
        "latitude": 37.386,
        "longitude": -122.0838
    }

    request = GeoRequest(ip_or_url="8.8.8.8")
    geolocation_service = GeolocationService()
    data = await geolocation_service.get_geolocation(request)

    assert data is not None
    assert data.country == "United States"
    assert data.city == "Mountain View"