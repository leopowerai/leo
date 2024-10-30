from enum import Enum
from typing import List, Optional

from db_handler import BaseDBHandler
from profile_generator import Student
from project_assigner import Project


# Define Enum for Complexity
class Complexity(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


# Define Enum for Status # NOT USED FOR NOW
class Status(Enum):
    OPEN = "open"
    IN_PROGRESS = "in progress"
    DONE = "done"
    BLOCKED = "blocked"
    IN_REVIEW = "in review"


# Define ProductBacklogItem class
class ProductBacklogItem:
    def __init__(
        self,
        id: str,
        title: str,
        description: str,
        story_points: int,
        stack: List[str],
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
        self.stack = stack
        self.assigned_to = assigned_to
        self.status = status
        self.project = project

    def set_assigned_to(self, new_assigned_to) -> None:
        # Process for updating ticket in here
        self.assigned_to = new_assigned_to

    def set_status(self, new_status) -> None:
        # Process for updating ticket in here
        self.status = new_status

    def assign(self, student, handler):
        # Update in notion
        success, result = handler.update_pbi(
            pbi_id=self.id,
            status=Status.IN_PROGRESS.value,
            owners=[student.platzi_username],
        )
        if success:
            print(f"Updated PBI:{self.title}: {result}")
        else:
            print(f"Failed to update PBI: {self.title}")

    def __repr__(self):
        return (
            f"ProductBacklogItem(title={self.title}, ID: {self.id}, description={self.description}, "
            f"story_points={self.story_points}, stack={self.stack}, "
            f"assigned_to={self.assigned_to}, status={self.status.value})"
        )


class PBIAssigner:
    def __init__(
        self,
        student: Student,
        project: Project,
        project_match_techs: List[str],
        pbis: List[ProductBacklogItem],
        db_handler: BaseDBHandler,  # This could be a parent class, NotionHandler is the child
    ):
        self.student = student
        self.project = project
        self.project_match_techs = project_match_techs
        self.pbis = pbis
        self.db_handler = db_handler

    def assign_pbi_to_student(self):
        """
        TODO: The PBIs need to be related to the project, perhaphs that could be a method within the Project class
        """

        for pbi in self.pbis:
            # print(f"PBI status: {pbi.status}")
            # print(f"PBI Assigned to: {pbi.assigned_to}")
            if pbi.status == Status.OPEN and pbi.assigned_to is None:
                # print(f"Match techs: {self.project_match_techs}")
                # print(f"PBI stack: {pbi.stack}")
                for match_tech in self.project_match_techs:

                    if match_tech in pbi.stack:
                        # Assign ticket
                        pbi.assign(self.student, self.db_handler)
                        return pbi

        return None
