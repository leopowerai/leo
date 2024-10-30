import os

from notion_client import Client

# Initialize the Notion client
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_PROJECT_DATABASE_ID = os.getenv("NOTION_PROJECT_DATABASE_ID")
notion = Client(auth=NOTION_API_KEY)


def read_notion_projects():
    response = notion.databases.query(database_id=NOTION_PROJECT_DATABASE_ID)
    projects = response.get("results", [])
    return projects


# Function to print information about each project
def print_project_info(project):
    properties = project.get("properties", {})
    for name, prop in properties.items():
        # Adjust based on property type, e.g., title, status, etc.
        if prop["type"] == "title":
            title = prop["title"][0]["plain_text"] if prop["title"] else "No title"
            print(f"{name}: {title}")
        # Add more property types as needed


# Example: Fetch all projects
# projects = read_notion_projects()
# for p in projects:
#     print_project_info(p)
