from pydantic import BaseModel
from typing import List

class PathItemOut(BaseModel):
    concept_id: int
    concept_name: str
    status: str
    reason: str
    is_locked: bool

class LearningPathResponse(BaseModel):
    items: List[PathItemOut]

class ResourceOut(BaseModel):
    id: int
    resource_type: str
    title: str
    content: str

class ConceptDetailResponse(BaseModel):
    id: int
    name: str
    description: str
    resources: List[ResourceOut]
    mastery_status: str

class PracticeSubmitRequest(BaseModel):
    question_id: int
    answer: str

class PracticeResultResponse(BaseModel):
    is_correct: bool
    correct_answer: str
    explanation: str
    new_mastery_score: float
