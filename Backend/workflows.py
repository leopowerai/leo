import logging

from notion_connector.notion_handler import NotionHandler
from pbi_assigner import PBIAssigner, ProductBacklogItem
from profile_generator import Student
from project_assigner import Project, ProjectAssigner

# Configure logging
logging.basicConfig(level=logging.INFO)


def assign_workflow(platzi_url, github_url):

    if not platzi_url or not github_url:
        response_dict = {"error": "Ambos campos son requeridos"}
        response_code = 400
        return response_dict, response_code

    # Get the student
    student = Student(platzi_url, github_url)

    if not student.profiles_exist():
        no_profile_text = "No se encontraron los perfiles de Platzi o GitHub"
        logging.info(no_profile_text)
        response_dict = {"message": no_profile_text}
        response_code = 404
        return response_dict, response_code

    # Bulk project instantiation from Notion ESTO PUEDE IR DENTRO DE NotionHandler
    notion_handler = NotionHandler()
    notion_projects = notion_handler.read_projects()
    formatted_projects = []

    for notion_project in notion_projects:
        formatted_projects.append(Project(*notion_project))

    project_assigner = ProjectAssigner(student, formatted_projects)
    project_match, selected_project, selected_tech = (
        project_assigner.find_project_for_student()
    )

    if project_match:
        logging.info(
            f"Match de proyecto {selected_project.name} con {selected_tech} tech, para el estudiante {student.platzi_username}"
        )

        # Get the PBIs from the project ESTO PUEDE IR DENTRO DE NotionHandler
        notion_pbis = notion_handler.read_pbis(selected_project.id)
        formatted_pbis = []
        for notion_pbi in notion_pbis:
            formatted_pbis.append(ProductBacklogItem(*notion_pbi))

        # Product Backlog Item assign
        pbi_assigner = PBIAssigner(
            student=student,
            project=selected_project,
            project_match_techs=[selected_tech],
            pbis=formatted_pbis,
            db_handler=notion_handler,
        )

        assigned_pbi = pbi_assigner.assign_pbi_to_student()
        if assigned_pbi:
            message = f"Se asignó el PBI: {assigned_pbi.title}"
            logging.info(message)
            response_dict = {
                "message": message,
                "iframe_url": f"https://v2-embednotion.com/12e3386028bd8066a3afe385ed758696?p={assigned_pbi.id}",
            }
            response_code = 200
        else:
            message = "No se encontró PBI para asignar"
            logging.info(message)
            response_dict = {"error": message}
            response_code = 400
            return response_dict, response_code

    else:
        message = (
            f"No hubo match de proyecto para el estudiante {student.platzi_username}"
        )
        logging.info(message)
        response_dict = {"error": message}
        response_code = 400
        return response_dict, response_code
