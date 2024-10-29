from project_assigner import check_profile_project_match

from profile_generator import fetch_profile_info


def main():
    # Get student profile
    profile: str = fetch_profile_info("https://platzi.com/p/LuisManuel/")

    # Define project stack
    project_stack = ["Python", "Django", "JavaScript", "React"]

    # Check if the project matches the student skills
    project_match = check_profile_project_match(profile, project_stack)

    if project_match:
        print(f"Match de proyecto con {project_match}")
    else:
        print("No hubo match de proyecto")


if __name__ == "__main__":
    main()
