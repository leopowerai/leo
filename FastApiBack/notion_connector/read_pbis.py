# notion_connector/read_pbis.py

from config import settings

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

    # Log the filter for debugging
    # logging.info("Requesting PBIs with filters: %s", filters)

    # Make the request to Notion
    async with session.post(url, json={"filter": filters}, headers=headers) as response:
        if response.status == 200:
            data = await response.json()
            pbis = data.get("results", [])
            
            # Log the PBIs fetched for debugging
            # logging.info("Fetched PBIs: %s", pbis)

            if len(pbis) == 0:
                return None, None
            
            # Get the project ID for the first PBI
            assigned_pbi_id = pbis[0].get("id")
            assigned_project_id = pbis[0]['properties'].get('projects_test', {}).get('relation', [{}])[0].get('id')
            return assigned_project_id, assigned_pbi_id
        else:
            error_text = await response.text()
            # logging.info("Error fetching PBIs: %d, %s", response.status, error_text)
            return None, None
