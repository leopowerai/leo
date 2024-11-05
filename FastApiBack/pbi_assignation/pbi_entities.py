import asyncio
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from ai_utils import get_embedding
from project_assignation.project_entities import Project
from sklearn.metrics.pairwise import cosine_similarity


class Complexity(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class Status(Enum):
    OPEN = "open"
    IN_PROGRESS = "in progress"
    DONE = "done"
    BLOCKED = "blocked"
    IN_REVIEW = "in review"


# Update the assign method in ProductBacklogItem
class ProductBacklogItem:
    def __init__(
        self,
        id: str,
        title: str,
        description: str,
        story_points: int,
        skills: List[str],
        project: Project,
        status: Status = Status.OPEN,
        assigned_to: Optional[str] = None,
        complexity: Optional[Complexity] = None,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.story_points = story_points
        self.complexity = complexity
        self.skills = skills
        self.assigned_to = assigned_to
        self.status = status
        self.project = project

    async def set_assigned_to(self, new_assigned_to) -> None:
        # Process for updating ticket in here
        self.assigned_to = new_assigned_to

    async def set_status(self, new_status) -> None:
        # Process for updating ticket in here
        self.status = new_status

    async def assign(self, student, handler):
        # Update in notion asynchronously
        success, result = await handler.update_pbi(
            pbi_id=self.id,
            status=Status.IN_PROGRESS.value,
            owners=[student.platzi_username],
        )
        if success:
            print(f"Updated PBI:{self.title}: {result}")
        else:
            print(f"Failed to update PBI: {self.title}")

    async def __repr__(self):
        return (
            f"ProductBacklogItem(title={self.title}, ID: {self.id}, description={self.description}, "
            f"story_points={self.story_points}, skills={self.skills}, "
            f"assigned_to={self.assigned_to}, status={self.status.value})"
        )


class PBIAssigner:
    def __init__(self, student, project, pbis, db_handler):
        self.student = student
        self.project = project
        self.pbis = pbis
        self.db_handler = db_handler

    def get_available_pbis(self):
        available_pbis = []
        for pbi in self.pbis:
            if pbi.status == Status.OPEN and pbi.assigned_to is None:
                available_pbis.append(pbi)

        return available_pbis

    async def find_matching_task(self, course_embeddings):
        """
        Identify the best matching tasks (PBIs) within a project based on the student's courses.
        Returns:
            List[Tuple[ProductBacklogItem, float]]: The PBIs and their similarity scores.
        """
        available_pbis = self.get_available_pbis()

        # Collect all unique skills from available PBIs
        all_skills = set()
        for pbi in available_pbis:
            all_skills.update(pbi.skills)
        all_skills = list(all_skills)

        # Fetch embeddings for all unique skills in batch
        skill_embeddings = await get_embedding(all_skills)
        skill_to_embedding = dict(zip(all_skills, skill_embeddings))

        pbi_scores = []

        for pbi in available_pbis:
            # Get embeddings for the PBI's skills from the mapping
            requirement_embeddings = [skill_to_embedding[skill] for skill in pbi.skills]

            # Calculate similarity scores between each course and each task requirement
            scores = [
                cosine_similarity([course_embedding], [req_embedding])[0][0]
                for course_embedding in course_embeddings
                for req_embedding in requirement_embeddings
            ]

            # Compute the average similarity score for the task
            avg_score = np.mean(scores) if scores else 0
            pbi_scores.append((pbi, avg_score))

        # Sort PBIs by their match score in descending order
        pbi_scores.sort(key=lambda x: x[1], reverse=True)

        return pbi_scores

    async def assign_pbi_to_student(self, pbi: ProductBacklogItem):
        await pbi.assign(self.student, self.db_handler)
        return pbi
