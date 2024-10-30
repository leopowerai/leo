from notion_connector.read_pbis import read_notion_pbis_for_project
from notion_connector.read_projects import read_notion_projects
from notion_connector.update_pbi import update_notion_pbi
from pbi_assigner import Status


class NotionHandler:
    def __init__(self):
        # TODO: Get the env variables in here to make them available for all the methods
        pass

    def create_pbi():
        pass

    def update_pbi():
        update_notion_pbi()

    def read_projects(self):
        notion_projects = read_notion_projects()
        formatted_projects = []
        for project in notion_projects:
            formatted_projects.append(_extract_project_info(project))

        return formatted_projects

    def read_pbis(self, project_id):
        notion_pbis = read_notion_pbis_for_project(project_id)
        formatted_pbis = []
        for pbi in notion_pbis:
            formatted_pbis.append(_extract_pbi_info(pbi))

        return formatted_pbis


# Helper methods
def _extract_project_info(project):
    # Extract the project ID (top-level key "id")
    project_id = project.get("id", "No ID found")

    # Extract the technologies (within the "technologies" property)
    technologies_prop = project.get("properties", {}).get("technologies", {})
    technologies = [tech["name"] for tech in technologies_prop.get("multi_select", [])]

    # Extract the project name (within the "project_name" property)
    project_name_prop = project.get("properties", {}).get("project_name", {})
    project_name = project_name_prop.get("title", [{}])[0].get(
        "plain_text", "No Name found"
    )

    # Print or return the extracted data
    # print(f"Project ID: {project_id}")
    # print(f"Technologies: {technologies}")
    # print(f"Project Name: {project_name}")
    return project_id, project_name, technologies


def _extract_pbi_info(pbi_data):
    # Title
    title = (
        pbi_data.get("properties", {})
        .get("task", {})
        .get("title", [{}])[0]
        .get("plain_text", "No Title")
    )

    # Description
    description = (
        pbi_data.get("properties", {})
        .get("description", {})
        .get("rich_text", [{}])[0]
        .get("plain_text", "No Description")
    )

    # Complexity (story points)
    story_points = (
        pbi_data.get("properties", {}).get("story_points", {}).get("number", 0)
    )

    # Stack (technologies)
    stack_prop = (
        pbi_data.get("properties", {}).get("technologies", {}).get("multi_select", [])
    )
    stack = [tech["name"] for tech in stack_prop]

    # Project (relation ID)
    project_relation = (
        pbi_data.get("properties", {}).get("projects_test", {}).get("relation", [{}])
    )
    project = (
        project_relation[0].get("id", "No Project Linked")
        if project_relation
        else "No Project Linked"
    )

    # Status
    status_data = pbi_data.get("properties", {}).get("status", {})
    status_name = status_data.get("status", {}).get("name", "No Status")

    # Assigned To
    owners_prop = (
        pbi_data.get("properties", {}).get("owners", {}).get("multi_select", [])
    )
    assigned_to = owners_prop[0]["name"] if owners_prop else None

    return (
        title,
        description,
        story_points,
        stack,
        project,
        _get_status_enum(status_name),
        assigned_to,
    )


def _get_status_enum(notion_status_str):
    try:
        return Status(notion_status_str)  # Tries to map the string to the enum
    except ValueError:
        return None  # Or some default Status value if the string doesn't match
