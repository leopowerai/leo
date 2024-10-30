import json
import os

from notion_client import Client

# Initialize the Notion client
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_PBI_DATABASE_ID = os.getenv("NOTION_PBI_DATABASE_ID")
notion = Client(auth=NOTION_API_KEY)


# Function to fetch all pbis for a given project ID
def read_notion_pbis_for_project(project_id):
    response = notion.databases.query(
        database_id=NOTION_PBI_DATABASE_ID,
        filter={
            "property": "projects_test",  # Replace with your relation field's name
            "relation": {"contains": project_id},
        },
    )
    pbis = response.get("results", [])
    return pbis


# Function to print information about each pbi
def print_pbi_info(pbi):
    properties = pbi.get("properties", {})
    for name, prop in properties.items():
        # Adjust based on property type, e.g., title, status, etc.
        if prop["type"] == "title":
            title = prop["title"][0]["plain_text"] if prop["title"] else "No title"
            # print(f"{name}: {title}")
        # Add more property types as needed


# Example: Fetch pbis for a specific project ID
# project_id = "12e3386028bd8066a3afe385ed758696"  # Replace with the ID of the project
# pbis = read_notion_pbis_for_project(project_id)

# print_pbi_info(pbis[0])
