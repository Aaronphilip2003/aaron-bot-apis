from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

class Database:
    client: AsyncIOMotorClient = None
    db_name: str = "Cluster0"

db = Database()

async def get_database() -> AsyncIOMotorClient:
    return db.client[db.db_name]

async def connect_to_mongo():
    """
    Create database connection.
    """
    mongo_uri = os.getenv("MONGO_URI")
    db.client = AsyncIOMotorClient(mongo_uri)
    print("Connected to MongoDB")

async def close_mongo_connection():
    """
    Close database connection.
    """
    if db.client is not None:
        db.client.close()
        print("MongoDB connection closed")
