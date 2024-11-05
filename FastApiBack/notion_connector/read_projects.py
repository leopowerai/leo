import asyncio
import datetime
import json
import logging
import os

import aiohttp
from config import settings
from redis_client import redis

NOTION_API_KEY = settings.NOTION_API_KEY
NOTION_PROJECT_DATABASE_ID = settings.NOTION_PROJECT_DATABASE_ID
NOTION_VERSION = "2022-06-28"


async def read_notion_projects(session):

    cache_key = "notion_projects"
    try:
        cached_data = await redis.get(cache_key)
        if cached_data:
            return json.loads(cached_data)
    except Exception as e:
        logging.warning(f"Redis error: {e}")

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

            # Cache the projects in Redis with an expiry time (e.g., 24 hours)
            try:
                await redis.set(cache_key, json.dumps(projects), ex=86400)
            except Exception as e:
                logging.warning(f"Redis error: {e}")
                # Proceed without caching if Redis is unavailable

            return projects
        else:
            error_text = await response.text()
            raise Exception(f"Error fetching projects: {response.status}, {error_text}")
