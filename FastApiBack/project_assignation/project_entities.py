from dataclasses import dataclass
from typing import List, Optional
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from ai_utils import get_embedding
from profile_generation.profile_entities import Student
from typing import List, Tuple, Dict, Any

@dataclass
class Project:
    id : str
    name : str
    skills : List[str]
    business_context: str
    technical_context: str
    company_name: str
    company_context: str


class ProjectAssigner:
    def __init__(self, projects: List[Project]):
        self.projects = projects
        self.requirements_embeddings_list: Dict[str, List[List[Any]]] = {}

    def calculate_projects_requirements_embeddings(self) -> None:
        # Iterate over each project to calculate similarity scores
        requirement_embeddings_list = {}
        for project in self.projects:
            # Generate embeddings for each requirement in the project
            requirement_embeddings = [get_embedding(
                req) for req in project.skills]
            requirement_embeddings_list[project.name] = requirement_embeddings
        self.requirements_embeddings_list = requirement_embeddings_list


    # Function to find the best matching projects based on course embeddings
    def find_matching_projects(self, student: Student):
        """
        Identify projects that best match the provided courses based on cosine similarity.

        Args:
            courses (List[str]): List of course names or descriptions.
            projects (List[Dict[str, Any]]): List of projects, each with requirements to match.

        Returns:
            List[Tuple[str, float]]: Sorted list of projects with their average similarity scores.
        """
        if(self.requirements_embeddings_list == {}):
            self.calculate_projects_requirements_embeddings()


        # Generate embeddings for each course
        course_embeddings = [get_embedding(course) for course in student.courses]

        # Store projects and their match scores
        project_scores = []

        # Iterate over each project to calculate similarity scores
        for project in self.projects:
            # Generate embeddings for each requirement in the project
            requirement_embeddings = self.requirements_embeddings_list[project.name]

            # Calculate similarity scores between each course and each project requirement
            scores = [
                cosine_similarity([course_embedding], [req_embedding])[0][0]
                for course_embedding in course_embeddings
                for req_embedding in requirement_embeddings
            ]

            # Compute the average similarity score for the project
            avg_score = np.mean(scores)
            project_scores.append((project, avg_score))

        # Sort projects by their match score in descending order
        project_scores.sort(key=lambda x: x[1], reverse=True)

        return project_scores, course_embeddings