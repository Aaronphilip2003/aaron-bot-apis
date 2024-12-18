from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.time_model import TimeEntry
import google.generativeai as genai
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pytz
from dateutil import parser

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

ENTRIES_COLLECTION = "entries"
TAGS_COLLECTION = "tags"

async def time_entries_service(query: TimeEntry, db: AsyncIOMotorDatabase):
    # Query the tags database for the tags and get all tags in a list
    tags_collection = db[TAGS_COLLECTION]
    tags = await tags_collection.find({}).to_list(length=100)
    
    tag_list = [tag["tag"] for tag in tags]
    
    prompt = f"Understand the following query {query.query} and return the most relevant tags from this {tag_list}. Just give me the names of the tags from {tag_list}. Make sure that you return from this list and nothing else with it. If it is not relevant then return the most relevant tags from this list, never return anything except tags from this list. The answer you return should have nothing else except tag from {tag_list} and nothing else. If you are not sure then return the most relevant tags from {tag_list}.Make sure that they are separated by commas and nothing else."
    response = model.generate_content(prompt)

    # convert the response to a list of strings and remove trailing things
    tag_list = response.text.split(",")
    relevant_tags = [tag.strip() for tag in tag_list]
    print(relevant_tags)

    # now from these relevant_tags, get me all the entries that match only these tags
    entries_collection = db[ENTRIES_COLLECTION]
    entries = await entries_collection.find({"tags": {"$in": relevant_tags}}).to_list(length=100)
    
    # entries_list = [entry["content"] for entry in entries]
    entries_list = [entry["timestamp"] for entry in entries]

    for i in range(len(entries_list)):
        entries_list[i] = convert_to_ist(entries_list[i])
    
    return entries_list

def convert_to_ist(iso_timestamp):
    ist_timezone = pytz.timezone("Asia/Kolkata")
    # If the input is already a datetime object, use it directly
    if isinstance(iso_timestamp, datetime):
        utc_time = iso_timestamp
    else:
        # Parse the ISO timestamp if it's a string
        utc_time = parser.isoparse(iso_timestamp)
    
    # Convert UTC to IST
    ist_time = utc_time.astimezone(ist_timezone)
    # Return formatted IST time
    return ist_time.strftime("%Y-%m-%d %H:%M:%S")