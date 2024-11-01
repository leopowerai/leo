from typing import List, Optional

from profile_generator import Student


class Project:
    def __init__(self, id, name, stack):
        self.id = id
        self.name = name
        self.stack = stack


class ProjectAssigner:
    def __init__(self, student: Student, projects: List[Project]):
        self.projects = projects
        self.student = student

    def find_project_for_student(self) -> Optional[str]:
        """
        TODO: In here, we need to be careful with the match with the technologies
        For now it is simply taking the first one that is on the project tags
        and the user profile
        """
        profile = self.student.platzi_profile_str
        for project in self.projects:
            matching_tech = self._check_profile_project_match(profile, project.stack)
            if matching_tech:
                return True, project, matching_tech
        return False, None, None

    def _check_profile_project_match(self, profile, project_stack) -> Optional[str]:
        """
        Searches for the first occurrence of any keyword in the provided text.

        Parameters:
        text (str): The text to search within.
        keywords (List[str]): A list of keywords to search for.

        Returns:
        Optional[str]: The first keyword found in the text, or None if no keywords are found.
        """
        for tech in project_stack:
            if tech in profile:
                return tech
        return None
