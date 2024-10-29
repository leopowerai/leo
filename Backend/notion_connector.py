import datetime

from notion_client import Client

# Initialize the Notion client
notion = Client(auth="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")

# Replace with your database ID (you can get this from the Notion board URL)
DATABASE_ID = "12e3386028bd817abbb5d696d604fa17"


# 1. Create a new task
# def create_task(title, description, deadline, tags):
#     deadline_date = deadline.isoformat() if deadline else None
#     response = notion.pages.create(
#         parent={"database_id": DATABASE_ID},
#         properties={
#             # "Name": {"title": [{"text": {"content": title}}]},
#             "Description": {"text": [{"text": {"content": description}}]},
#             # "Deadline": {"date": {"start": deadline_date}},
#             # "Tags": {"multi_select": [{"name": tag} for tag in tags]}
#         }
#     )
#     return response


def create_task(description):
    # Ensure that description is provided as a list of rich text objects
    description_property = {"rich_text": [{"text": {"content": description}}]}

    # Create the page in the specified database
    response = notion.pages.create(
        parent={"database_id": DATABASE_ID},
        properties={
            "Description": description_property  # Replace with your actual property name
        },
    )
    return response


# 2. Update an existing task by its page_id
def update_task(page_id, title=None, description=None, deadline=None, tags=None):
    properties = {}
    if title:
        properties["Name"] = {"title": [{"text": {"content": title}}]}
    if description:
        properties["Description"] = {"rich_text": [{"text": {"content": description}}]}
    if deadline:
        properties["Deadline"] = {"date": {"start": deadline.isoformat()}}
    if tags:
        properties["Tags"] = {"multi_select": [{"name": tag} for tag in tags]}

    response = notion.pages.update(page_id=page_id, properties=properties)
    return response


# 3. Delete a task by updating its status or using a custom delete function
def delete_task(page_id):
    # Notion API does not support hard deletion, but you can mark it as archived
    response = notion.pages.update(page_id=page_id, archived=True)
    return response


# Example Usage
# Set your task parameters
task_title = "Finish Python Script"
task_description = "Mostrar funcionamiento de Notion"
task_deadline = datetime.datetime(2024, 11, 1)
task_tags = ["Python", "Notion", "API"]

# Create a new task
new_task = create_task(task_description)
print("Created Task:", new_task)

# # Update the task (replace `new_task["id"]` with the actual page ID of the task)
# updated_task = update_task(new_task["id"], description="Updated description", tags=["Updated"])
# print("Updated Task:", updated_task)

# # Delete the task
# deleted_task = delete_task(new_task["id"])
# print("Deleted Task:", deleted_task)
