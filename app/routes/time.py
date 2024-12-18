from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.time_model import TimeEntry
from services.time_service import time_entries_service
from database import get_database

router = APIRouter()

@router.post("/")
async def time_entries(
    query: TimeEntry,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Query the knowledge base for entries.
    """
    response = await time_entries_service(query, db)
    return response