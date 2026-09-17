from pydantic import BaseModel
from typing import List, Optional

class OptionOut(BaseModel):
    id: int
    label: str
    text: str

class QuestionOut(BaseModel):
    id: int
    text: str
    question_type: str
    concept_name: str
    difficulty: int
    options: List[OptionOut] = []

class AssessmentStartResponse(BaseModel):
    assessment_id: int
    questions: List[QuestionOut]

class SubmitItem(BaseModel):
    question_id: int
    answer: str

class SubmitRequest(BaseModel):
    responses: List[SubmitItem]

class AssessmentReportResponse(BaseModel):
    score: float
    concept_mastery: dict
    root_cause_analysis: list
    recommendations: list
