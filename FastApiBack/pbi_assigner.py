from enum import Enum
from typing import List, Optional


from project_assigner import Project

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

class PBIAssigner:
    def __init__(self, student, project, project_match_techs, pbis, db_handler):
        self.student = student
        self.project = project
        self.project_match_techs = project_match_techs
        self.pbis = pbis
        self.db_handler = db_handler

    async def assign_pbi_to_student(self):
        for pbi in self.pbis:
            if pbi.status == Status.OPEN and pbi.assigned_to is None:
                for match_tech in self.project_match_techs:
                    if match_tech in pbi.stack:
                        # Assign ticket
                        await pbi.assign(self.student, self.db_handler)
                        return pbi
        return None

# Update the assign method in ProductBacklogItem
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
            f"story_points={self.story_points}, stack={self.stack}, "
            f"assigned_to={self.assigned_to}, status={self.status.value})"
        )
