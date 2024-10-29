from enum import Enum
from typing import List, Optional

from profile_generator import Student
from project_assigner import Project


# Define Enum for Complexity
class Complexity(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


# Define Enum for Status
class Status(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    BLOCKED = "blocked"
    IN_REVIEW = "in_review"


# Define ProductBacklogItem class
class ProductBacklogItem:
    def __init__(
        self,
        title: str,
        description: str,
        complexity: Complexity,
        stack: List[str],
        project: Project,
        status: Status = Status.OPEN,
        assigned_to: Optional[str] = None,
    ):
        self.title = title
        self.description = description
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

    def __repr__(self):
        return (
            f"ProductBacklogItem(title={self.title}, description={self.description}, "
            f"complexity={self.complexity.value}, stack={self.stack}, "
            f"assigned_to={self.assigned_to}, status={self.status.value})"
        )


class PBIAssigner:
    def __init__(
        self,
        student: Student,
        project: Project,
        project_match_techs: List[str],
        pbis: List[ProductBacklogItem],
    ):
        self.student = student
        self.project = project
        self.project_match_techs = project_match_techs
        self.pbis = pbis

    def assign_pbi_to_student(self):
        """
        TODO: The PBIs need to be related to the project, perhaphs that could be a method within the Project class
        """

        for pbi in self.pbis:
            if pbi.status == Status.OPEN and pbi.assigned_to is None:
                for match_tech in self.project_match_techs:
                    if match_tech in pbi.stack:
                        # Assign ticket
                        pbi.set_assigned_to(self.student)
                        pbi.set_status(Status.IN_PROGRESS)

                        return pbi

        return None
