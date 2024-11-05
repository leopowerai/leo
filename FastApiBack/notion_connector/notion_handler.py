# notion_handler.py

import aiohttp
from db_handler import BaseDBHandler
from pbi_assignation.pbi_entities import Status
from notion_connector.read_pbis import read_notion_pbis_for_project, get_filtered_pbis_for_student
from notion_connector.read_projects import read_notion_projects
from notion_connector.update_pbi import update_notion_pbi

class NotionHandler(BaseDBHandler):
    def __init__(self):
        super().__init__()
        # self.session = aiohttp.ClientSession()
        self.session = self.open_session()
    
    def open_session(self):
        self.session = aiohttp.ClientSession()
        return self.session

    async def close(self):
        await self.session.close()

    async def create_pbi(self, **kwargs):
        """
        Create a new Product Backlog Item (PBI) in Notion.
        For now, this method is a placeholder to satisfy the abstract base class requirements.
        """
        # Placeholder implementation
        raise NotImplementedError("create_pbi method is not implemented yet.")

    async def update_pbi(self, pbi_id, **kwargs):
        success, result = await update_notion_pbi(self.session, pbi_id, **kwargs)
        return success, result

    async def read_projects(self):
        notion_projects = await read_notion_projects(self.session)
        formatted_projects = [self._extract_project_info(project) for project in notion_projects]
        return formatted_projects

    async def read_pbis(self, project_id):
        notion_pbis = await read_notion_pbis_for_project(self.session, project_id)
        formatted_pbis = [self._extract_pbi_info(pbi) for pbi in notion_pbis]
        return formatted_pbis

    # Helper methods
    def _extract_project_info(self, project):
        # Extract the project ID
        project_id = project.get("id", "No ID found")

        # Extract the skills
        skills_prop = project.get("properties", {}).get("skills", {})
        skills = [tech["name"] for tech in skills_prop.get("multi_select", [])]

        # Extract the project name
        project_name_prop = project.get("properties", {}).get("project_name", {})
        project_name = project_name_prop.get("title", [{}])[0].get("plain_text", "No Name found")

        # Extract the company name (or default if not found)
        company_prop = project.get("properties", {}).get("company_name", {})
        company_name = company_prop.get("rich_text", [{}])[0].get("plain_text", "The Chill Company")

        # Extract the business context
        business_context_prop = project.get("properties", {}).get("business_context", {})
        business_context = business_context_prop.get("rich_text", [{}])[0].get("plain_text", "")

        # Extract the technical context
        technical_context_prop = project.get("properties", {}).get("technical_context", {})
        technical_context = technical_context_prop.get("rich_text", [{}])[0].get("plain_text", "")

        # Extract the company context
        company_context_prop = project.get("properties", {}).get("company_context", {})
        company_context = company_context_prop.get("rich_text", [{}])[0].get("plain_text", "")

        # Return all required fields
        return (
            project_id,
            project_name,
            skills,
            business_context,
            technical_context,
            company_name,
            company_context
        )

    def _extract_pbi_info(self, pbi_data):
        # Extract the PBI ID
        pbi_id = pbi_data.get("id", "No ID found")

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

        # Stack (skills)
        stack_prop = (
            pbi_data.get("properties", {}).get("skills", {}).get("multi_select", [])
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
            pbi_id,
            title,
            description,
            story_points,
            stack,
            project,
            self._get_status_enum(status_name),
            assigned_to,
        )

    def _get_status_enum(self, notion_status_str):
        try:
            return Status(notion_status_str.lower().replace(" ", "_"))
        except ValueError:
            return None  # Or some default Status value if the string doesn't match
    

    async def is_student_assigned_to_open_pbi(self, student_username):
        assigned_project_id, assigned_pbi_id = await get_filtered_pbis_for_student(self.session, student_username)

        # If any PBIs are returned, the student is assigned to at least one PBI in those statuses
        return assigned_project_id, assigned_pbi_id


