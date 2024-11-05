import asyncio  # Import asyncio
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

import numpy as np
from ai_utils import get_embedding
from profile_generation.profile_entities import Student
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class Project:
    id: str
    name: str
    skills: List[str]
    business_context: str
    technical_context: str
    company_name: str
    company_context: str


class ProjectAssigner:
    def __init__(self, projects: List[Project]):
        self.projects = projects
        self.requirements_embeddings_list: Dict[str, List[List[Any]]] = {}

    async def calculate_projects_requirements_embeddings(self) -> None:
        requirement_embeddings_list = {}
        for project in self.projects:
            # Create a list of coroutines for get_embedding
            tasks = [get_embedding(req) for req in project.skills]
            # Run the coroutines concurrently
            requirement_embeddings = await asyncio.gather(*tasks)
            requirement_embeddings_list[project.name] = requirement_embeddings
        self.requirements_embeddings_list = requirement_embeddings_list

    async def find_matching_projects(self, student: Student):
        """
        Identify projects that best match the provided courses based on cosine similarity.

        Returns:
            List[Tuple[Project, float]]: Sorted list of projects with their average similarity scores.
        """
        if not self.requirements_embeddings_list:
            await self.calculate_projects_requirements_embeddings()

        # Generate embeddings for each course
        course_tasks = [get_embedding(course) for course in student.courses]
        course_embeddings = await asyncio.gather(*course_tasks)

        project_scores = []

        for project in self.projects:
            requirement_embeddings = self.requirements_embeddings_list[project.name]

            # Calculate similarity scores between each course and each project requirement
            scores = [
                cosine_similarity([course_embedding], [req_embedding])[0][0]
                for course_embedding in course_embeddings
                for req_embedding in requirement_embeddings
            ]

            # Compute the average similarity score for the project
            avg_score = np.mean(scores) if scores else 0
            project_scores.append((project, avg_score))

        # Sort projects by their match score in descending order
        project_scores.sort(key=lambda x: x[1], reverse=True)

        return project_scores, course_embeddings
