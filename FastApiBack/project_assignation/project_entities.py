# project_entities.py
import asyncio
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
        # Collect all unique skills
        all_skills = set()
        for project in self.projects:
            all_skills.update(project.skills)
        all_skills = list(all_skills)

        # Fetch embeddings in batch
        skill_embeddings = await get_embedding(all_skills)

        # Map skills to embeddings
        skill_to_embedding = dict(zip(all_skills, skill_embeddings))

        # Build the requirements embeddings list for each project
        for project in self.projects:
            requirement_embeddings = [
                skill_to_embedding[skill] for skill in project.skills
            ]
            self.requirements_embeddings_list[project.name] = requirement_embeddings

    async def find_matching_projects(self, student: Student):
        if not self.requirements_embeddings_list:
            await self.calculate_projects_requirements_embeddings()

        # Fetch course embeddings in batch
        course_embeddings = await get_embedding(student.courses)

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
