# workflows.py

import logging

from notion_connector.notion_handler import NotionHandler
from pbi_assigner import PBIAssigner, ProductBacklogItem
from profile_generator import Student
from project_assigner import Project, ProjectAssigner


async def assign_workflow(platzi_url, github_url):
    logging.info("Assign workflow started")
    if not platzi_url or not github_url:
        response_dict = {"error": "Ambos campos son requeridos"}
        response_code = 400
        return response_dict, response_code

    # Get the student
    student = Student(platzi_url, github_url)

    if not await student.profiles_exist():
        no_profile_text = "No se encontraron los perfiles de Platzi o GitHub"
        logging.info(no_profile_text)
        response_dict = {"message": no_profile_text}
        response_code = 400
        return response_dict, response_code

    # Instantiate NotionHandler
    notion_handler = NotionHandler()

    try:
        # Read projects from Notion
        logging.info("Reading projects from Notion")
        notion_projects = await notion_handler.read_projects()
        formatted_projects = [Project(*project) for project in notion_projects]

        # Assign project to student
        logging.info(f"Assigning project to student {student.platzi_username}")
        project_assigner = ProjectAssigner(student, formatted_projects)
        project_match, selected_project, selected_tech = (
            project_assigner.find_project_for_student()
        )

        if project_match:
            logging.info(
                f"Match de proyecto {selected_project.name} con {selected_tech} tech, para el estudiante {student.platzi_username}"
            )

            # Read PBIs for the selected project
            logging.info(f"Reading PBIs for project {selected_project.id}")
            notion_pbis = await notion_handler.read_pbis(selected_project.id)
            formatted_pbis = [ProductBacklogItem(*pbi) for pbi in notion_pbis]

            # Assign PBI to student
            pbi_assigner = PBIAssigner(
                student=student,
                project=selected_project,
                project_match_techs=[selected_tech],
                pbis=formatted_pbis,
                db_handler=notion_handler,
            )
            logging.info(f"Assigning PBI to {student.platzi_username}")
            assigned_pbi = await pbi_assigner.assign_pbi_to_student()
            if assigned_pbi:
                message = f"Se asignó el PBI: {assigned_pbi.title}"
                logging.info(message)
                f_project_id = remove_char(selected_project.id, "-")
                f_pbi_id = remove_char(assigned_pbi.id, "-")

                response_dict = {
                    "message": message,
                    "pbiId": assigned_pbi.id,
                    "iframe_url": f"https://v2-embednotion.com/theffs/{f_project_id}?p={f_pbi_id}&pm=s",
                }
                response_code = 200
                return response_dict, response_code
            else:
                message = "No se encontró PBI para asignar"
                logging.info(message)
                response_dict = {"error": message}
                response_code = 400
                return response_dict, response_code
        else:
            message = f"No hubo match de proyecto para el estudiante {student.platzi_username}"
            logging.info(message)
            response_dict = {"error": message}
            response_code = 400
            return response_dict, response_code
    finally:
        await notion_handler.close()


def remove_char(string, character):
    return string.replace(character, "")
