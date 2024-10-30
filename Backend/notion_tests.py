from notion_connector.notion_handler import NotionHandler
from pbi_assigner import PBIAssigner, ProductBacklogItem
from profile_generator import Student
from project_assigner import Project, ProjectAssigner

# Get the student
platzi_url = "https://platzi.com/p/LuisManuel/"
github_url = "https://github.com/LuisMa9L/"
student = Student(platzi_url, github_url)


# Bulk project instantiation from Notion ESTO PUEDE IR DENTRO DE NotionHandler
notion_handler = NotionHandler()
notion_projects = notion_handler.read_projects()
formatted_projects = []

for notion_project in notion_projects:
    formatted_projects.append(Project(*notion_project))

if not student.profiles_exist():
    print("No se encontraron los perfiles de Platzi o GitHub")
else:
    project_assigner = ProjectAssigner(student, formatted_projects)
    project_match, selected_project, selected_tech = (
        project_assigner.find_project_for_student()
    )

    if project_match:
        print(
            f"Match de proyecto {selected_project.name} con {selected_tech} tech, para el estudiante {student.platzi_username}"
        )

        # Get the PBIs from the project ESTO PUEDE IR DENTRO DE NotionHandler
        notion_pbis = notion_handler.read_pbis(selected_project.id)
        formatted_pbis = []
        for notion_pbi in notion_pbis:
            formatted_pbis.append(ProductBacklogItem(*notion_pbi))

        print(formatted_pbis)

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
            print(f"Se asignó el ticket: {assigned_pbi.title}")
        else:
            print("No se encontró ticket para asignar")

    else:
        print("No hubo match de proyecto")
