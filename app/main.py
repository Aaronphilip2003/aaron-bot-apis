from fastapi import FastAPI
from routes import add, query, time
from database import connect_to_mongo, close_mongo_connection

# Initialize FastAPI app
app = FastAPI(title="Aaron Bot API", version="1.0")

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

# Include routes
app.include_router(add.router, prefix="/add", tags=["Add"])
app.include_router(query.router, prefix="/query", tags=["Query"])
app.include_router(time.router, prefix="/time", tags=["Time"])
# app.include_router(tags.router, prefix="/tags", tags=["Tags"])
# app.include_router(suggest.router, prefix="/suggest", tags=["Suggest"])

# /query: Think of it like a search engine for your knowledge base — “What exactly have I written down about XYZ?”
# /suggest: Think of it as your personal assistant — “Analyze what I’ve done and tell me what I should do next.”