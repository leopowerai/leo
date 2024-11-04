import asyncio
import datetime
import json
import os
from config import settings
import aiohttp

NOTION_API_KEY = settings.NOTION_API_KEY
NOTION_PROJECT_DATABASE_ID = settings.NOTION_PROJECT_DATABASE_ID
NOTION_VERSION = "2022-06-28"

CACHE_FILE = "notion_projects_cache.json"
CACHE_EXPIRY_HOURS = 24  # Adjust cache duration as needed

async def read_notion_projects(session):
    # Check if cached data exists and is recent
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                cached_data = json.load(f)
                cache_timestamp = datetime.datetime.fromisoformat(cached_data.get("timestamp", ""))
                
                # If cache is still valid, return cached projects
                if datetime.datetime.now() - cache_timestamp < datetime.timedelta(hours=CACHE_EXPIRY_HOURS):
                    return cached_data["projects"]
                
        except (json.JSONDecodeError, ValueError):  # Handle empty or corrupted cache file
            print("Cache file is empty or corrupted. Fetching new data...")
            os.remove(CACHE_FILE)  # Remove the corrupted cache file to allow fresh fetching

    # If no valid cache, fetch from Notion API
    url = f"https://api.notion.com/v1/databases/{NOTION_PROJECT_DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }

    filter_payload = {
        "filter": {
            "property": "status",
            "status": {"equals": "in progress"},
        }
    }

    async with session.post(url, headers=headers, json=filter_payload) as response:
        if response.status == 200:
            data = await response.json()
            projects = data.get("results", [])
            
            # Save the new data to cache
            with open(CACHE_FILE, "w") as f:
                json.dump({"timestamp": datetime.datetime.now().isoformat(), "projects": projects}, f)
                
            return projects
        else:
            error_text = await response.text()
            raise Exception(f"Error fetching projects: {response.status}, {error_text}")
