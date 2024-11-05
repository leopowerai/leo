# workflows/assign.py

import logging

from ai_utils import get_embedding  # Import get_embedding for batch embeddings
from notion_connector.notion_handler import NotionHandler
from pbi_assignation.pbi_entities import PBIAssigner, ProductBacklogItem
from profile_generation.profile_entities import Student
from project_assignation.project_entities import Project, ProjectAssigner
from utils import remove_char


# This function assigns a project and PBIs to a student
async def assign_project_and_pbi(
    notion_handler: NotionHandler,
    project_assigner: ProjectAssigner,
    platzi_url,
    github_url,
    recommended_pbis_count=1,
):
    logging.info("Assign workflow started")

    notion_handler.open_session()
    if not platzi_url or not github_url:
        response_dict = {
            "error": "Both 'username' and 'github_url' fields are required"
        }
        response_code = 400
        return response_dict, response_code

    # Create the Student object
    student = Student(platzi_url, github_url)

    # Check if the student's profiles exist
    if not await student.profile_exists():
        no_profile_text = "Platzi or GitHub profiles not found"
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

        # Fetch course embeddings in batch
        course_embeddings = await get_embedding(student.courses)

        # Find matching projects using batch embeddings
        recommended_projects, _ = await project_assigner.find_matching_projects(student)

        if not recommended_projects:
            no_project_text = "No recommended projects found"
            logging.info(no_project_text)
            response_dict = {"message": no_project_text}
            response_code = 400
            return response_dict, response_code

        # Select the top recommended project
        selected_project = recommended_projects[0][0]
        logging.info(f"Recommended project: {selected_project.name}")

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

        # Find matching PBIs using batch embeddings
        scored_pbis = await pbi_assigner.find_matching_task(course_embeddings)

        if not scored_pbis:
            message = "No recommended PBIs found"
            logging.info(message)
            response_dict = {"message": message}
            response_code = 400
            return response_dict, response_code

        # Adjust the number of recommended PBIs if necessary
        if recommended_pbis_count > len(scored_pbis):
            recommended_pbis_count = len(scored_pbis)

        # Prepare the list of recommended PBIs
        recommended_pbis = []
        for i in range(recommended_pbis_count):
            pbi = scored_pbis[i][0]
            score = scored_pbis[i][1]
            rec_pbi = {
                "pbiId": remove_char(pbi.id, "-"),
                "pbiTitle": pbi.title,
                "pbiDescription": pbi.description,
                "pbiSkills": pbi.skills,
                "pbiScore": score * 100,  # Assuming the score is between 0 and 1
            }
            recommended_pbis.append(rec_pbi)

        # Prepare the response
        f_project_id = remove_char(selected_project.id, "-")
        response_dict = {
            "message": "Project assigned and PBIs suggested",
            "projectId": f_project_id,
            "projectName": selected_project.name,
            "projectSkills": selected_project.skills,
            "projectBusinessContext": selected_project.business_context,
            "projectTechnicalContext": selected_project.technical_context,
            "companyName": selected_project.company_name,
            "companyContext": selected_project.company_context,
            "suggestedPbis": recommended_pbis,
        }
        response_code = 200
        return response_dict, response_code

    finally:
        await notion_handler.close()
