from profile_generator import Student
from project_assigner import Project, ProjectAssigner


def main():

    try:
        # Get the projects
        project1 = Project(
            name="Test Project 1", stack=["Python", "Django", "JavaScript", "React"]
        )
        projects = [project1]

        # Get the student
        platzi_url = "https://platzi.com/p/LuisManuel/"
        github_url = "https://github.com/LuisMa9L/"
        student = Student(platzi_url, github_url)

        if not student.profiles_exist():
            print("No se encontraron los perfiles de Platzi o GitHub")
        else:
            project_assigner = ProjectAssigner(student, projects)
            project_match = project_assigner.find_project_for_student()

            if project_match:
                print(
                    f"Match de proyecto {project_match[0].name} con {project_match[1]} tech, para el estudiante {student.platzi_username}"
                )
            else:
                print("No hubo match de proyecto")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
