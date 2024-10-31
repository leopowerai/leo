import os

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_PROJECT_DATABASE_ID = os.getenv("NOTION_PROJECT_DATABASE_ID")
NOTION_VERSION = "2022-06-28"


async def create_pbi(self, **kwargs):
    """
    Create a new Product Backlog Item (PBI) in Notion.
    """
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }
    # Prepare the data for the new PBI
    data = {
        "parent": {"database_id": 1},
        "properties": {
            # Fill in the necessary properties using kwargs
        },
    }
    async with self.session.post(url, json=data, headers=headers) as response:
        if response.status == 200:
            result = await response.json()
            return result
        else:
            error_text = await response.text()
            raise Exception(f"Error creating PBI: {response.status}, {error_text}")
