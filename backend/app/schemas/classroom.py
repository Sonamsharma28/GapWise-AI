from pydantic import BaseModel
from typing import Optional, List

class CreateClassRequest(BaseModel):
    name: str
    grade: str = "Class 10"
    subject: str = "Mathematics"
    class_code: Optional[str] = None
    description: Optional[str] = None

class JoinClassRequest(BaseModel):
    class_code: str

class ClassStudentSummary(BaseModel):
    id: int
    name: str
    email: str
    overall_mastery: float
    joined_at: str

class ClassroomResponse(BaseModel):
    id: int
    name: str
    grade: str
    subject: str
    class_code: str
    description: Optional[str] = None
    teacher_name: str
    student_count: int
    avg_mastery: float
    created_at: str
    share_link: str
