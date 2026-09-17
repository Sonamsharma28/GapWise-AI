from pydantic import BaseModel
from typing import List

class MasteryItem(BaseModel):
    concept_id: int
    concept_name: str
    score: float
    status: str

class DashboardResponse(BaseModel):
    name: str
    overall_score: float
    recent_mastery: List[MasteryItem]
