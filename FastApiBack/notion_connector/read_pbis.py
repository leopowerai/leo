# notion_connector/read_pbis.py

import os
import aiohttp
import asyncio

NOTION_API_KEY =  #os.getenv("NOTION_API_KEY")
NOTION_PBI_DATABASE_ID =  # os.getenv("NOTION_PBI_DATABASE_ID")
NOTION_VERSION = "2022-06-28"  # Use the latest supported version

async def read_notion_pbis_for_project(session, project_id):
    url = f"https://api.notion.com/v1/databases/{NOTION_PBI_DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }
    payload = {
        "filter": {
            "property": "projects_test",
            "relation": {"contains": project_id},
        }
    }

    async with session.post(url, json=payload, headers=headers) as response:
        if response.status == 200:
            data = await response.json()
            pbis = data.get("results", [])
            return pbis
        else:
            error_text = await response.text()
            raise Exception(f"Error fetching PBIs: {response.status}, {error_text}")
