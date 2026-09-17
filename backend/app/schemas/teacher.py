from pydantic import BaseModel
from typing import List

class StudentSummary(BaseModel):
    id: int
    name: str
    overall_score: float
    weak_concepts: List[str]

class TeacherDashboardResponse(BaseModel):
    students: List[StudentSummary]

class StudentDetailResponse(BaseModel):
    id: int
    name: str
    mastery: List[dict]
