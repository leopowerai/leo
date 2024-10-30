import os
from datetime import datetime, timedelta

from notion_client import Client

# Initialize the Notion client
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
notion = Client(auth=NOTION_API_KEY)


def update_notion_pbi(
    page_id, status=None, owners=None, update_due_date=False, url_pr=None, feedback=None
):
    # Prepare the properties to update
    update_data = {}

    # Update the status if provided
    if status:
        update_data["status"] = {"status": {"name": status}}

    # Update the owners if provided
    if owners:
        # Prepare the data for the multi-select update
        updated_owners = [{"name": name} for name in owners]
        update_data["owners"] = {"multi_select": updated_owners}

    # Update the due date to one week from today if requested
    if update_due_date:
        due_date = (datetime.today() + timedelta(weeks=1)).strftime("%Y-%m-%d")
        update_data["final_date"] = {"date": {"start": due_date}}

    # Update the URL if provided
    if url_pr:
        update_data["url_pr"] = {"url": url_pr}

    # Update the feedback if provided
    if feedback:
        update_data["feedback"] = {"rich_text": [{"text": {"content": feedback}}]}

    # Attempt to update the page with the specified properties
    try:
        response = notion.pages.update(page_id=page_id, properties=update_data)
        print("Item updated successfully:", response)
    except Exception as e:
        print("Failed to update item:", e)


# Example usage of the update_pbi function
# page_id = "12e3386028bd8194a1ebc61fa6922160"  # Replace with the actual page ID of the pbi to update
# status = "En curso"
# owners = ["Alguarito"]
# update_due_date = True
# url_pr = "https://github.com/sldkfldsk"
# feedback = "Deberias vender bianchi en un semaforo"

# update_notion_pbi(
#     page_id,
#     status=status,
#     owners=owners,
#     update_due_date=update_due_date,
#     url_pr=url_pr,
#     feedback=feedback,
# )
