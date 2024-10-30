# notion_connector/update_pbi.py

import os
import aiohttp
from datetime import timedelta, datetime

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_VERSION = "2022-06-28"

async def update_notion_pbi(
    session,
    pbi_id,
    status=None,
    owners=None,
    update_due_date=False,
    url_pr=None,
    feedback=None,
):
    url = f"https://api.notion.com/v1/pages/{pbi_id}"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }

    # Prepare the properties to update
    update_data = {"properties": {}}

    # Update the status if provided
    if status:
        update_data["properties"]["status"] = {"status": {"name": status}}

    # Update the owners if provided
    if owners:
        # Prepare the data for the multi-select update
        updated_owners = [{"name": name} for name in owners]
        update_data["properties"]["owners"] = {"multi_select": updated_owners}

    # Update the due date to one week from today if requested
    if update_due_date:
        due_date = (datetime.today() + timedelta(weeks=1)).strftime("%Y-%m-%d")
        update_data["properties"]["final_date"] = {"date": {"start": due_date}}

    # Update the URL if provided
    if url_pr:
        update_data["properties"]["url_pr"] = {"url": url_pr}

    # Update the feedback if provided
    if feedback:
        update_data["properties"]["feedback"] = {
            "rich_text": [{"text": {"content": feedback}}]
        }

    async with session.patch(url, json=update_data, headers=headers) as response:
        if response.status == 200:
            data = await response.json()
            print("Item updated successfully")
            return True, data
        else:
            error_text = await response.text()
            print("Failed to update item:", error_text)
            return False, None
