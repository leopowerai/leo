# notion_connector/read_projects.py

import asyncio
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

    # Define the filter payload
    filter_payload = {
        "filter": {
            "property": "status",  # Make sure this matches the name of your status property in Notion
            "status": {"equals": "in progress"},  # The status you want to filter by
        }
    }

    # Include the filter in the POST request
    async with session.post(url, headers=headers, json=filter_payload) as response:
        if response.status == 200:
            data = await response.json()
            projects = data.get("results", [])
            return projects
        else:
            error_text = await response.text()
            raise Exception(f"Error fetching projects: {response.status}, {error_text}")


# Tests
async def test_read_projects():
    async with aiohttp.ClientSession() as session:
        projects = await read_notion_projects(session)
        for project in projects:
            # Extract the project's name
            project_name = project["properties"]["project_name"]["title"][0]["text"][
                "content"
            ]
            print(f"Project Name: {project_name}")
