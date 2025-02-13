from typing import List, Union

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.geolocation import (
    get_geolocation_by_ip_or_url,
    create_geolocation,
    delete_geolocation as delete_geolocation_db,
    get_all_geolocations,
    get_geolocation_by_id,
)
from app.schemas.geolocation import GeoLocationResponse, GeoRequest
from app.db import database
from app.services.geolocation import get_geolocation

router = APIRouter()


@router.post("/geolocation", response_model=GeoLocationResponse,
             summary="Add a geolocation record",
             description="Fetches geolocation data from an external API and stores it in the database. "
                         "If the IP or URL already exists, returns HTTP 409 Conflict."
             )
async def add_geolocation(request: GeoRequest, db: AsyncSession = Depends(database.get_db)):
    existing_entry = await get_geolocation_by_ip_or_url(db, ip_or_url=request.ip_or_url)
    if existing_entry:
        raise HTTPException(status_code=409, detail="Geolocation record already exists")
    data = await get_geolocation(request)
    if not data:
        raise HTTPException(status_code=400, detail="Invalid IP address or URL")
    return await create_geolocation(db, data)


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
):
    if id and ip_or_url:
        raise HTTPException(status_code=400, detail="Provide either id or ip_or_url, not both.")

    if id:
        data = await get_geolocation_by_id(db, id)
    elif ip_or_url:
        data = await get_geolocation_by_ip_or_url(db, ip_or_url)
    else:
        return await get_all_geolocations(db)

    if not data:
        raise HTTPException(status_code=404, detail="Data not found")

    return data


@router.delete("/geolocation/{id}",
               summary="Delete geolocation by ID",
               description="Deletes a geolocation record from the database using its unique ID. "
                           "Returns a success message if the deletion was successful."
               )
async def delete_geolocation(db: AsyncSession = Depends(database.get_db), id: int = None):
    deleted = await delete_geolocation_db(db=db, id=id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Data not found")
    return {"message": "Successfully deleted"}
