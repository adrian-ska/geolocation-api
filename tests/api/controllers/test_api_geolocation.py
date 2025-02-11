import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch


# Test client for synchronous API requests
@pytest.fixture(scope="module")
def test_client():
    """Provides a synchronous FastAPI test client."""
    with TestClient(app) as client:
        yield client


# Test client for asynchronous API requests
@pytest_asyncio.fixture(scope="module")
async def async_client():
    """Provides an asynchronous HTTPX test client for API testing."""
    transport = ASGITransport(app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


# Mock response for IPStack API
def mock_ipstack_response():
    return {
        "ip": "8.8.8.8",
        "country_name": "United States",
        "region_name": "California",
        "city": "Mountain View",
        "latitude": 37.3861,
        "longitude": -122.0839,
    }


# Helper function to add a test geolocation record
async def add_test_geolocation(client, ip):
    return await client.post("/geolocation", json={"ip_or_url": ip})


@pytest.mark.asyncio
@patch("app.clients.ipstack.IPStackClient.fetch_geolocation", new_callable=AsyncMock)
async def test_add_geolocation(mock_ipstack, async_client):
    """Tests if adding geolocation data for an IP address works correctly."""
    mock_ipstack.return_value = mock_ipstack_response()
    response = await add_test_geolocation(async_client, ip="8.8.8.8")

    assert response.status_code == 200
    data = response.json()

    expected_fields = {"id", "ip_or_url", "country", "latitude", "longitude", "region", "city"}
    assert expected_fields.issubset(data.keys()), f"Missing fields: {expected_fields - data.keys()}"


@pytest.mark.asyncio
@patch("app.clients.ipstack.IPStackClient.fetch_geolocation", new_callable=AsyncMock)
async def test_get_geolocation_by_ip(mock_ipstack, async_client):
    """Tests retrieving geolocation data using an IP address."""
    mock_ipstack.return_value = mock_ipstack_response()

    # Add a test record
    await add_test_geolocation(async_client, ip="8.8.8.8")

    # Retrieve geolocation data
    response = await async_client.get("/geolocation?ip_or_url=8.8.8.8")
    assert response.status_code == 200
    data = response.json()

    assert data["ip_or_url"] == "8.8.8.8"
    assert data["country"] == "United States"
    assert data["region"] == "California"
    assert data["city"] == "Mountain View"
    assert isinstance(data["latitude"], float)
    assert isinstance(data["longitude"], float)


@pytest.mark.asyncio
@patch("app.clients.ipstack.IPStackClient.fetch_geolocation", new_callable=AsyncMock)
async def test_get_all_geolocations(mock_ipstack, async_client):
    """Tests retrieving all stored geolocation records."""
    mock_ipstack.return_value = mock_ipstack_response()

    # Add test records to the database
    await add_test_geolocation(async_client, ip="8.8.8.8")
    await add_test_geolocation(async_client, ip="1.1.1.1")

    # Fetch all geolocation records
    response = await async_client.get("/geolocation")
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list), "Response should be a list"
    assert len(data) >= 2, "At least two geolocation records should exist"

    expected_fields = {"id", "ip_or_url", "country", "latitude", "longitude", "region", "city"}
    for record in data:
        assert expected_fields.issubset(record.keys()), f"Missing fields: {expected_fields - record.keys()}"


@pytest.mark.asyncio
@patch("app.clients.ipstack.IPStackClient.fetch_geolocation", new_callable=AsyncMock)
async def test_get_geolocation_by_id(mock_ipstack, async_client):
    """Tests retrieving a geolocation record using its unique ID."""
    mock_ipstack.return_value = mock_ipstack_response()

    # Add a test record
    await add_test_geolocation(async_client, ip="8.8.8.8")

    # Retrieve all records to obtain an ID
    response_all = await async_client.get("/geolocation")
    assert response_all.status_code == 200
    data_all = response_all.json()
    assert len(data_all) > 0, "There should be at least one geolocation record"

    test_id = data_all[0]["id"]

    # Fetch a specific record by ID
    response = await async_client.get(f"/geolocation?id={test_id}")
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == test_id
    assert "ip_or_url" in data
    assert "country" in data
    assert isinstance(data["latitude"], float)
    assert isinstance(data["longitude"], float)
