# notion_connector/read_projects.py

import os

import aiohttp

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_PROJECT_DATABASE_ID = os.getenv("NOTION_PROJECT_DATABASE_ID")
NOTION_VERSION = "2022-06-28"


async def read_notion_projects(session):
    url = f"https://api.notion.com/v1/databases/{NOTION_PROJECT_DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }

    async with session.post(url, headers=headers) as response:
        if response.status == 200:
            data = await response.json()
            projects = data.get("results", [])
            return projects
        else:
            error_text = await response.text()
            raise Exception(f"Error fetching projects: {response.status}, {error_text}")
