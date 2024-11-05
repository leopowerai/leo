# notion_connector/update_pbi.py

import os
import aiohttp
from datetime import timedelta, datetime
from config import settings
import logging

NOTION_API_KEY = settings.NOTION_API_KEY
NOTION_VERSION = "2022-06-28"

async def update_notion_pbi(
    session,
    pbi_id,
    status=None,
    owners=None,
    update_due_date=False,
    results_url=None,
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

    if owners is not None:
        if owners:  # If owners list is not empty
            updated_owners = [{"name": name} for name in owners]
            update_data["properties"]["owners"] = {"multi_select": updated_owners}
        else:  # Clear the multi-select field by setting it to an empty list
            update_data["properties"]["owners"] = {"multi_select": []}

    # Update the due date to one week from today if requested
    if update_due_date:
        due_date = (datetime.today() + timedelta(weeks=2)).strftime("%Y-%m-%d")
        update_data["properties"]["final_date"] = {"date": {"start": due_date}}

    # Update the URL if provided
    if results_url:
        update_data["properties"]["results_url"] = {"url": results_url}

    # Update the feedback if provided
    if feedback:
        update_data["properties"]["feedback"] = {
            "rich_text": [{"text": {"content": feedback}}]
        }

    async with session.patch(url, json=update_data, headers=headers) as response:
        if response.status == 200:
            data = await response.json()
            
            logging.info(f"Item updated successfully")
            return True, data
        else:
            error_text = await response.text()
            logging.info("Failed to update item:", error_text)
            return False, None
