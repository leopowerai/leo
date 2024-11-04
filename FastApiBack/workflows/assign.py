# workflows.py

import logging

from utils import remove_char
from notion_connector.notion_handler import NotionHandler
from pbi_assignation.pbi_entities import PBIAssigner, ProductBacklogItem
from profile_generation.profile_entities import Student
from project_assignation.project_entities import Project, ProjectAssigner


# TODO: This func should be split into two functions (one for the project assigner and one for the PBI assigner)
async def assign_project_and_pbi(notion_handler: NotionHandler,
                                 project_assigner: ProjectAssigner,
                                 platzi_url, 
                                 github_url,
                                 recommended_pbis_count = 1):
    
    logging.info("Assign workflow started")

    notion_handler.open_session()
    if not platzi_url or not github_url:
        response_dict = {"error": "Ambos campos son requeridos"}
        response_code = 400
        return response_dict, response_code

    # Get the student
    student = Student(platzi_url, github_url)

    # Check if both profiles exist
    if not await student.profile_exists():
        no_profile_text = "No se encontraron los perfiles de Platzi o GitHub"
        logging.info(no_profile_text)
        response_dict = {"message": no_profile_text}
        response_code = 400
        return response_dict, response_code

    try:
        success, message = await student.fetch_student_courses()
        if not success:
            logging.info(message)
            response_dict = {"error": message}
            response_code = 400
            return response_dict, response_code

        # Assign project to student
        logging.info(f"Assigning project to student {student.platzi_username}")

        recommended_projects, course_embeddings = (
            project_assigner.find_matching_projects(student)
        )

        if not recommended_projects or not course_embeddings:
            no_project_text = "No se encontraron proyectos recomendados"
            logging.info(no_project_text)
            response_dict = {"message": no_project_text}
            response_code = 400
            return response_dict, response_code
        
        # AQUI PODRIAMOS SUGERIR VARIOS PROYECTOS
        selected_project = max(recommended_projects, key=lambda x: x[1])[0]
        logging.info(f"Proyecto recomendado: {selected_project.name}")
        

        # Read PBIs for the selected project
        logging.info(f"Reading PBIs for project {selected_project.id}")
        notion_pbis = await notion_handler.read_pbis(selected_project.id)
        formatted_pbis = [ProductBacklogItem(*pbi) for pbi in notion_pbis]

        # Assign PBI to student
        pbi_assigner = PBIAssigner(
            student=student,
            project=selected_project,
            pbis=formatted_pbis,
            db_handler=notion_handler,
        )

        logging.info(f"Assigning PBI to {student.platzi_username}")
        scored_pbis = await pbi_assigner.find_matching_task(course_embeddings)
        if (len(scored_pbis) == 0):
            message = "No se encontraron PBIs recomendados"
            logging.info(message)
            response_dict = {"message": message}
            response_code = 400
            return response_dict, response_code
        
        # selected_pbi = max(recommended_pbis, key=lambda x: x[1])[0]
        # print(f"Recommended PBI: {recommended_pbis[0][0].title}")
        # print(f"Recommended PBI: {recommended_pbis[1][0].title}")
        # print(f"Recommended PBI: {recommended_pbis[2][0].title}")
        if (recommended_pbis_count > len(scored_pbis)):
            recommended_pbis_count = len(scored_pbis)
        
        recommended_pbis = []
        for i in range(recommended_pbis_count):
            rec_pbi = {
                "pbiId": remove_char(scored_pbis[i][0].id, "-"),
                "pbiTitle": scored_pbis[i][0].title,
                "pbiDescription": scored_pbis[i][0].description,
                "pbiSkills": scored_pbis[i][0].skills,
                "pbiScore": scored_pbis[i][1]*100
            }
            recommended_pbis.append(rec_pbi)

        # El proceso de seleccion de PBI ahora se hace por aparte

        # await pbi_assigner.assign_pbi_to_student(selected_pbi)
        # message = f"Se asignó el PBI: {selected_pbi.title}"
        # print(message)
        # logging.info(message)
        f_project_id = remove_char(selected_project.id, "-")

        response_dict = {
            "message": "Se asigno el proyecto y se sugirieron los PBIs",
            "projectId": f_project_id,
            "projectName": selected_project.name,
            "projectSkills": selected_project.skills,
            "projectBusinessContext": selected_project.business_context,
            "projectTechnicalContext": selected_project.technical_context,
            "companyName": selected_project.company_name,
            "companyContext": selected_project.company_context,
            "suggestedPbis": [dict(pbi) for pbi in recommended_pbis]
            # "iframeUrl": f"https://v2-embednotion.com/theffs/{f_project_id}?p={f_pbi_id}&pm=s",
        }
        response_code = 200
        return response_dict, response_code

    finally:
        await notion_handler.close()
