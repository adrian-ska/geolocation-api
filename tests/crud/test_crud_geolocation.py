import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import geolocation as crud
from app.schemas import geolocation as schemas


@pytest.mark.asyncio
async def test_create_geolocation_success(setup_database: AsyncSession):
    """Test creating a new geolocation record (POST)"""
    db = setup_database

    geolocation = schemas.GeoLocationResponse(
        id=1,
        ip_or_url="8.8.8.8",
        country="United States",
        region="California",
        city="Mountain View",
        latitude="37.386",
        longitude="-122.0838"
    )

    created = await crud.create_geolocation(db, geolocation)

    assert created is not None, "Failed to create geolocation record."
    assert created.ip_or_url == "8.8.8.8", "Saved IP address does not match."


@pytest.mark.asyncio
async def test_get_geolocation_success(setup_database: AsyncSession):
    """Test retrieving an existing geolocation record (GET)"""
    db = setup_database

    geolocation = schemas.GeoLocationResponse(
        id=1,
        ip_or_url="1.1.1.1",
        country="Australia",
        region="Queensland",
        city="Brisbane",
        latitude="-27.4705",
        longitude="153.026"
    )
    await crud.create_geolocation(db, geolocation)

    fetched = await crud.get_geolocation_by_ip_or_url(db, "1.1.1.1")

    assert fetched is not None, "Geolocation record not found in the database."
    assert fetched.ip_or_url == "1.1.1.1", "Returned IP address is incorrect."


@pytest.mark.asyncio
async def test_get_geolocation_fail_not_found(setup_database: AsyncSession):
    """Test retrieving a non-existent geolocation record (GET)"""
    db = setup_database

    fetched = await crud.get_geolocation_by_ip_or_url(db, "3.3.3.3")

    assert fetched is None, "Expected no data, but found a record."


@pytest.mark.asyncio
async def test_delete_geolocation_success(setup_database: AsyncSession):
    """Test successfully deleting a geolocation record (DELETE)"""
    db = setup_database

    geolocation = schemas.GeoLocationResponse(
        id=1,
        ip_or_url="2.2.2.2",
        country="Germany",
        region="Berlin",
        city="Berlin",
        latitude="52.5200",
        longitude="13.4050"
    )
    await crud.create_geolocation(db, geolocation)

    await crud.delete_geolocation(db, id=1)

    fetched = await crud.get_geolocation_by_ip_or_url(db, ip_or_url="2.2.2.2")

    assert fetched is None, "Geolocation record was not deleted."


@pytest.mark.asyncio
async def test_delete_geolocation_fail_not_found(setup_database: AsyncSession):
    """Test deleting a non-existent geolocation record (DELETE)"""
    db = setup_database

    with pytest.raises(HTTPException) as exc_info:
        await crud.delete_geolocation(db, id=999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Geolocation not found"