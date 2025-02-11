from typing import Optional, List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from app.models.geolocation import GeoLocation
from app.schemas.geolocation import GeoLocationResponse
from app.core.logger import logger


def log_and_raise_exception(message: str, status_code: int):
    """Logs an error message and raises an HTTP exception."""
    logger.error(message)
    raise HTTPException(status_code=status_code, detail=message)


async def get_geolocation(
    db: AsyncSession, key: str, value: str | int
) -> Optional[GeoLocation]:
    """Fetches a geolocation record based on a given key (either 'id' or 'ip_or_url')."""
    try:
        result = await db.execute(select(GeoLocation).where(getattr(GeoLocation, key) == value))
        return result.scalar_one_or_none()
    except SQLAlchemyError as e:
        log_and_raise_exception(f"Database error while retrieving geolocation ({key}={value}): {e}", 500)


async def get_geolocation_by_ip_or_url(db: AsyncSession, ip_or_url: str) -> Optional[GeoLocation]:
    """Fetches a geolocation record based on the provided IP or URL."""
    return await get_geolocation(db, "ip_or_url", ip_or_url)


async def get_geolocation_by_id(db: AsyncSession, id: int) -> Optional[GeoLocation]:
    """Retrieves a geolocation entry from the database using its unique ID."""
    return await get_geolocation(db, "id", id)


async def get_all_geolocations(db: AsyncSession) -> List[GeoLocation]:
    """Returns all geolocation records stored in the database."""
    try:
        result = await db.execute(select(GeoLocation))
        return result.scalars().all()
    except SQLAlchemyError as e:
        log_and_raise_exception(f"Database error while retrieving all geolocations: {e}", 500)


async def create_geolocation(db: AsyncSession, data: GeoLocationResponse) -> GeoLocation:
    """Creates and stores a new geolocation entry in the database."""
    try:
        db_entry = GeoLocation(**data.model_dump())  # Convert Pydantic model to dictionary
        db.add(db_entry)
        await db.commit()
        await db.refresh(db_entry)
        return db_entry
    except SQLAlchemyError as e:
        log_and_raise_exception(f"Database error while creating geolocation: {e}", 500)


async def delete_geolocation(db: AsyncSession, id: int) -> bool:
    """Deletes a geolocation entry by its ID. Returns True if successful."""
    entry = await get_geolocation_by_id(db, id)
    if not entry:
        logger.warning("Geolocation not found in database.")
        raise HTTPException(status_code=404, detail="Geolocation not found")
    try:
        await db.delete(entry)
        await db.commit()
        return True
    except SQLAlchemyError as e:
        log_and_raise_exception(f"Database error while deleting geolocation: {e}", 500)
