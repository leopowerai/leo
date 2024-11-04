import asyncio
from notion_connector.notion_handler import NotionHandler
from profile_generation.profile_entities import Student
from config import settings # Load env vars
from workflows.assign import assign_project_and_pbi
from workflows.startup import preload_projects


# Tests
async def test_profile():
    platzi_profile_url = "https://platzi.com/p/LuisManuel/"  # Replace with a valid Platzi profile
    github_profile_url = "https://github.com/LuisMa9L/"         # Replace with a valid GitHub profile
    student = Student(platzi_profile_url, github_profile_url)
    profiles_exist = await student.profiles_exist()

    if profiles_exist:
        print("Profile data fetched successfully!")
        print("Platzi Username:", student.platzi_username)
        print("Platzi Profile JSON Data:", student.platzi_profile_str)
    else:
        print("One or both profiles do not exist.")

# asyncio.run(test_profile())

async def test_assign_flow():
    platzi_profile_url = "https://platzi.com/p/LuisManuel/"  # Replace with a valid Platzi profile
    github_profile_url = "https://github.com/LuisMa9L/"
    
    # Preload projects
    notion_handler = NotionHandler()
    project_assigner = await preload_projects(notion_handler)

    # Assign project and PBI
    await assign_project_and_pbi(notion_handler, project_assigner, platzi_profile_url, github_profile_url)
asyncio.run(test_assign_flow())