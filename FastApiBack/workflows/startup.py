"""
This workflow is used to preload the project data
and calculate the embeddings for the project requirements
"""

import logging

from project_assignation.project_entities import Project, ProjectAssigner
from notion_connector.notion_handler import NotionHandler

async def preload_projects(notion_handler: NotionHandler) -> ProjectAssigner:
    logging.info("Preloading projects")

    # Read projects from Notion
    notion_projects = await notion_handler.read_projects()
    formatted_projects = [Project(*project) for project in notion_projects]

    # Calculate embeddings for project requirements
    project_assigner = ProjectAssigner(formatted_projects)
    project_assigner.calculate_projects_requirements_embeddings()

    return project_assigner
    