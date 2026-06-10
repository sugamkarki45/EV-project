from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.db import get_db
from app.models.models import ChargerListing
from typing import List, Optional

router = APIRouter()

@router.get("/")
async def list_listings(
    db: AsyncSession = Depends(get_db),
    lat: Optional[float] = None,
    lng: Optional[float] = None,
    radius: Optional[float] = 5.0
):
    result = await db.execute(select(ChargerListing))
    listings = result.scalars().all()
    return listings

@router.post("/")
async def create_listing(listing: dict, db: AsyncSession = Depends(get_db)):
    # In real app, convert dict to model and save
    return {"message": "Listing created and pending approval"}
