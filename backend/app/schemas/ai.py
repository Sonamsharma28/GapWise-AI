from pydantic import BaseModel
from typing import Optional, Any, List

class MentorRequest(BaseModel):
    message: str
    concept_id: Optional[int] = None
    question_id: Optional[int] = None
    question_num: Optional[int] = None

class MentorResponse(BaseModel):
    response: str
    suggested_concept: Optional[Any] = None
    question_id: Optional[int] = None
    context_used: Optional[List[str]] = []

class OptionDetail(BaseModel):
    label: str
    text: str
    is_correct: bool

class QuestionExplanationResponse(BaseModel):
    question_num: Optional[int] = None
    question_id: int
    question_text: str
    concept_id: Optional[int] = None
    concept_name: str
    student_answer_label: Optional[str] = None
    student_answer_text: Optional[str] = None
    correct_answer_label: str
    correct_answer_text: str
    all_options: List[OptionDetail] = []
    why_wrong: str
    step_by_step: List[str]
    golden_rule: str
    mini_challenge: str
    teacher_tip: Optional[str] = None
