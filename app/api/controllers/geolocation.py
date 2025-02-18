from typing import List, Union

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.geolocation import GeolocationCRUD
from app.schemas.geolocation import GeoLocationResponse, GeoRequest
from app.db import database
from app.services.geolocation import GeolocationService

router = APIRouter()


@router.post("/geolocation", response_model=GeoLocationResponse,
             summary="Add a geolocation record",
             description="Fetches geolocation data from an external API and stores it in the database. "
                         "If the IP or URL already exists, returns HTTP 409 Conflict."
             )
async def add_geolocation(request: GeoRequest, db: AsyncSession = Depends(database.get_db),
                          geolocation_service: GeolocationService = Depends(GeolocationService),
                          crud: GeolocationCRUD = Depends(GeolocationCRUD)):
    try:
        existing_entry = await crud.get_geolocation_by_ip_or_url(db, ip_or_url=request.ip_or_url)
        if existing_entry:
            raise HTTPException(status_code=409, detail="Geolocation record already exists")
        data = await geolocation_service.get_geolocation(request)
        if not data:
            raise HTTPException(status_code=400, detail="Invalid IP address or URL")
        return await crud.create_geolocation(db, data)
    except SQLAlchemyError as exc:
        handle_db_exception(exc)

@router.get("/geolocation", response_model=Union[List[GeoLocationResponse], GeoLocationResponse],
            summary="Retrieve geolocation data",
            description="Fetches stored geolocation data from the database. "
                        "Can be filtered by `id` or `ip_or_url`. "
                        "If no parameters are provided, all records are returned."
            )
async def get_geolocation_data(
        id: int | None = None,
        ip_or_url: str | None = None,
        db: AsyncSession = Depends(database.get_db),
        crud: GeolocationCRUD = Depends(GeolocationCRUD)
):
    try:
        if id and ip_or_url:
            raise HTTPException(status_code=400, detail="Provide either id or ip_or_url, not both.")

        if id:
            data = await crud.get_geolocation_by_id(db, id)
        elif ip_or_url:
            data = await crud.get_geolocation_by_ip_or_url(db, ip_or_url)
        else:
            return await crud.get_all_geolocations(db)

        if not data:
            raise HTTPException(status_code=404, detail="Data not found")

        return data


    except SQLAlchemyError as exc:

        handle_db_exception(exc)


@router.delete("/geolocation/{id}",
               summary="Delete geolocation by ID",
               description="Deletes a geolocation record from the database using its unique ID. "
                           "Returns a success message if the deletion was successful."
               )
async def delete_geolocation(id: int, db: AsyncSession = Depends(database.get_db),
                             crud: GeolocationCRUD = Depends(GeolocationCRUD)):
    try:
        if not await crud.delete_geolocation(db, id):
            raise HTTPException(status_code=404, detail="Data not found")
        return {"message": "Successfully deleted"}



    except SQLAlchemyError as exc:

        handle_db_exception(exc)

def handle_db_exception(exc: SQLAlchemyError):
    if isinstance(exc, IntegrityError):
        raise HTTPException(status_code=400, detail="Database integrity error")
    elif isinstance(exc, OperationalError):
        raise HTTPException(status_code=503, detail="Database connection error")
    else:
        raise HTTPException(status_code=500, detail="Unexpected database error")
