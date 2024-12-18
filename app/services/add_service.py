from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.add_model import AddEntry
from datetime import datetime
from fastapi import HTTPException
from database import get_database

ENTRIES_COLLECTION = "entries"
TAGS_COLLECTION = "tags"

async def add_entry_service(entry_data: AddEntry, db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Add a new entry to the knowledge base and update tags.
    """
    entries_collection = db[ENTRIES_COLLECTION]
    tags_collection = db[TAGS_COLLECTION]

    # Prepare the entry data
    entry = {
        "content": entry_data.content,
        "tags": entry_data.tags,
        "metadata": entry_data.metadata or {},
        "timestamp": datetime.utcnow()
    }

    # Insert the entry into the "entries" collection
    result = await entries_collection.insert_one(entry)
    print(result, "inserted")

    # Add or update tags in the "tags" collection
    for tag in entry_data.tags:
        await tags_collection.update_one(
            {"tag": tag},
            {"$setOnInsert": {"tag": tag}},
            upsert=True
        )

    # Return success response
    if result.inserted_id:
        return {"message": "Entry added successfully!", "entry_id": str(result.inserted_id)}
    else:
        raise HTTPException(status_code=500, detail="Failed to add the entry.")

