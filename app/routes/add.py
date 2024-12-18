from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.add_model import AddEntry
from services.add_service import add_entry_service
from database import get_database

router = APIRouter()

@router.post("/")
async def add_new_entry(
    entry: AddEntry,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Add a new entry to the knowledge base.
    """
    response = await add_entry_service(entry, db)
    return response