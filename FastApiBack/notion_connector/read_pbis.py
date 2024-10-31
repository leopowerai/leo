# notion_connector/read_pbis.py

import asyncio
import os
from config import settings

import aiohttp

NOTION_API_KEY = settings.NOTION_API_KEY
NOTION_PBI_DATABASE_ID = settings.NOTION_PBI_DATABASE_ID
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


async def get_filtered_pbis_for_student(session, student_username):
    # Define the statuses to filter for
    target_statuses = ["open", "in progress", "in review"]
    
    url = f"https://api.notion.com/v1/databases/{settings.NOTION_PBI_DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {settings.NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }

    # Construct the filter to fetch PBIs by status and assigned owner
    filters = {
        "and": [
            {
                "or": [
                    {
                        "property": "status",
                        "status": {"equals": status}
                    } for status in target_statuses
                ]
            },
            {
                "property": "owners",
                "multi_select": {"contains": student_username}
            }
        ]
    }

    # Make the request to Notion
    async with session.post(url, json={"filter": filters}, headers=headers) as response:
        if response.status == 200:
            data = await response.json()
            pbis = data.get("results", [])
            return pbis
        else:
            error_text = await response.text()
            raise Exception(f"Error fetching PBIs: {response.status}, {error_text}")


    # Make the request to Notion
    async with session.post(url, json={"filter": filters}, headers=headers) as response:
        if response.status == 200:
            data = await response.json()
            pbis = data.get("results", [])
            
            # Filter PBIs to check if they are assigned to the student
            assigned_pbis = [
                pbi for pbi in pbis
                if student_username in [owner.get("name") for owner in pbi.get("owners", [])]
            ]
            return assigned_pbis
        else:
            error_text = await response.text()
            raise Exception(f"Error fetching PBIs: {response.status}, {error_text}")
