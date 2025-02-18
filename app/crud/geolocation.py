from typing import Optional, List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from app.models.geolocation import GeoLocation
from app.schemas.geolocation import GeoLocationResponse
from app.core.logger import logger

class GeolocationCRUD:
    @staticmethod
    def log_and_raise_exception(message: str, status_code: int):
        """Logs an error and raises an HTTP exception."""
        logger.error(message)
        raise HTTPException(status_code=status_code, detail=message)


    async def get_geolocation(self,
        db: AsyncSession, key: str, value: str | int
    ) -> Optional[GeoLocation]:
        """Fetches a geolocation entry by a given key ('id' or 'ip_or_url')."""
        try:
            result = await db.execute(select(GeoLocation).where(getattr(GeoLocation, key) == value))
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            self.log_and_raise_exception(f"DB error while fetching geolocation ({key}={value}): {e}", 500)


    async def get_geolocation_by_ip_or_url(self, db: AsyncSession, ip_or_url: str) -> Optional[GeoLocation]:
        """Finds a geolocation record by IP or URL."""
        return await self.get_geolocation(db, "ip_or_url", ip_or_url)


    async def get_geolocation_by_id(self, db: AsyncSession, id: int) -> Optional[GeoLocation]:
        """Finds a geolocation record by its ID."""
        return await self.get_geolocation(db, "id", id)


    async def get_all_geolocations(self, db: AsyncSession) -> List[GeoLocation]:
        """Retrieves all geolocation records from the database."""
        try:
            result = await db.execute(select(GeoLocation))
            return result.scalars().all()
        except SQLAlchemyError as e:
            self.log_and_raise_exception(f"DB error while fetching all geolocations: {e}", 500)


    async def create_geolocation(self, db: AsyncSession, data: GeoLocationResponse) -> GeoLocation:
        """Adds a new geolocation to the database."""
        try:
            db_entry = GeoLocation(**data.model_dump())
            db.add(db_entry)
            await db.commit()
            await db.refresh(db_entry)
            return db_entry
        except SQLAlchemyError as e:
            self.log_and_raise_exception(f"DB error while creating geolocation: {e}", 500)


    async def delete_geolocation(self, db: AsyncSession, id: int) -> bool:
        """Removes a geolocation entry by its ID."""
        entry = await self.get_geolocation_by_id(db, id)
        if not entry:
            logger.warning("Geolocation not found in DB.")
            raise HTTPException(status_code=404, detail="Geolocation not found")
        try:
            await db.delete(entry)
            await db.commit()
            return True
        except SQLAlchemyError as e:
            self.log_and_raise_exception(f"DB error while deleting geolocation: {e}", 500)