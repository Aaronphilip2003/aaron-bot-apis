from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.query_model import QueryEntry
from services.query_service import query_entries_service
from database import get_database

router = APIRouter()

@router.post("/")
async def query_entries(
    query: QueryEntry,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Query the knowledge base for entries.
    """
    response = await query_entries_service(query, db)
    return response