from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..middleware.auth import get_current_user, require_role
from ..schemas.ai import MentorRequest, MentorResponse, QuestionExplanationResponse
from ..services.ai_mentor import get_mentor_response, get_question_explanation

router = APIRouter(prefix="/api/ai", tags=["ai"])

@router.post("/mentor", response_model=MentorResponse)
def mentor(request: MentorRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    res = get_mentor_response(
        db,
        user.id,
        request.message,
        request.concept_id,
        request.question_id,
        request.question_num
    )
    return MentorResponse(**res)

@router.get("/explain/{question_id}", response_model=QuestionExplanationResponse)
def explain_question(
    question_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("student"))
):
    """
    Returns a fully structured AI explanation for a specific wrong question.
    Powers the inline WrongQuestionExplainer component on the dashboard and AI Mentor page.
    """
    result = get_question_explanation(db, user.id, question_id)
    if not result:
        raise HTTPException(status_code=404, detail="Question not found")
    return QuestionExplanationResponse(**result)
