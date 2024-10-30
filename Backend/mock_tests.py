from pbi_assigner import Complexity, PBIAssigner, ProductBacklogItem
from profile_generator import Student
from project_assigner import Project, ProjectAssigner


def main():

    try:
        # Get the projects
        project1 = Project(
            id="some-id",
            name="Test Project 1",
            stack=["Python", "Django", "JavaScript", "React"],
        )
        projects = [project1]

        # Project PBIs
        pbi1 = ProductBacklogItem(
            title="Tarea 1, de Python",
            description="Esta es la tarea de prueba 1",
            complexity=Complexity.LOW,
            stack=["Python", "OpenAI"],
            project=project1,
        )

        pbi2 = ProductBacklogItem(
            title="Tarea 2, de JS",
            description="Esta es la tarea de prueba 2",
            complexity=Complexity.LOW,
            stack=["JavaScript", "OpenAI"],
            project=project1,
        )

        pbis = [pbi1, pbi2]

        # Get the student
        platzi_url = "https://platzi.com/p/LuisManuel/"
        github_url = "https://github.com/LuisMa9L/"
        student = Student(platzi_url, github_url)

        if not student.profiles_exist():
            print("No se encontraron los perfiles de Platzi o GitHub")
        else:
            project_assigner = ProjectAssigner(student, projects)
            project_match, selected_project, selected_tech = (
                project_assigner.find_project_for_student()
            )

            if project_match:
                print(
                    f"Match de proyecto {selected_project.name} con {selected_tech} tech, para el estudiante {student.platzi_username}"
                )

                # Product Backlog Item assign
                pbi_assigner = PBIAssigner(
                    student=student,
                    project=project1,
                    project_match_techs=[selected_tech],
                    pbis=pbis,
                )

                assigned_pbi = pbi_assigner.assign_pbi_to_student()
                if assigned_pbi:
                    print(f"Se asignó el ticket {assigned_pbi.title}")
                else:
                    print("No se encontró ticket para asignar")

            else:
                print("No hubo match de proyecto")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
