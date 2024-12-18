from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

async def get_database_client():
    """
    Retrieve the MongoDB client instance for database operations.
    """
    # Retrieve the MongoDB URI from environment variable
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise HTTPException(status_code=500, detail="MONGO_URI not found in environment variables")
    
    # Create the MongoDB client
    client = AsyncIOMotorClient(mongo_uri)
    print(client, "connected")
    return client