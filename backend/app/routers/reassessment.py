from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..models.assessment import Assessment, AssessmentResponse
from ..models.question import Question, QuestionOption
from ..models.concept import Concept
from ..models.mastery import ConceptMastery
from ..middleware.auth import get_current_user, require_role
from ..services.gap_detection import analyze_assessment
from ..services.learning_path import generate_personalized_learning_path

router = APIRouter(prefix="/api/reassessment", tags=["reassessment"])

@router.post("/start")
def start_reassessment(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("student"))
):
    """
    Creates a focused reassessment targeting concepts that currently need improvement.
    """
    # Find concepts in developing or needs_attention
    weak_masteries = db.query(ConceptMastery).filter(
        ConceptMastery.student_id == user.id,
        ConceptMastery.status.in_(["needs_attention", "developing"])
    ).all()
    
    target_cids = [m.concept_id for m in weak_masteries]
    if not target_cids:
        # If all mastered, pick higher difficulty concepts
        target_cids = [c.id for c in db.query(Concept).all()[:6]]

    questions = db.query(Question).filter(Question.concept_id.in_(target_cids)).all()
    if not questions:
        questions = db.query(Question).limit(10).all()

    assessment = Assessment(
        student_id=user.id,
        assessment_type="reassessment",
        status="in_progress",
        created_at=datetime.now(timezone.utc)
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    q_list = []
    for q in questions:
        concept = db.query(Concept).filter_by(id=q.concept_id).first()
        options = db.query(QuestionOption).filter_by(question_id=q.id).order_by(QuestionOption.option_label).all()
        q_list.append({
            "id": q.id,
            "text": q.text,
            "type": q.question_type,
            "concept_name": concept.name if concept else "Mathematics",
            "concept_id": q.concept_id,
            "difficulty": q.difficulty,
            "options": [
                {
                    "id": opt.id,
                    "label": opt.option_label,
                    "text": opt.option_text
                }
                for opt in options
            ]
        })

    return {
        "id": assessment.id,
        "assessment_id": assessment.id,
        "questions": q_list
    }

@router.post("/{id}/submit")
def submit_reassessment(
    id: int,
    payload: dict = Body(...),
    db: Session = Depends(get_db),
    user: User = Depends(require_role("student"))
):
    assessment = db.query(Assessment).filter_by(id=id, student_id=user.id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Reassessment not found")

    # Snapshot previous mastery before analysis
    previous_mastery = {
        m.concept_id: {"score": m.score, "status": m.status}
        for m in db.query(ConceptMastery).filter_by(student_id=user.id).all()
    }

    # Extract answers
    answers_map = {}
    if "answers" in payload:
        answers_map = payload["answers"]
    elif "responses" in payload:
        for item in payload["responses"]:
            answers_map[item.get("question_id")] = item.get("answer")

    db.query(AssessmentResponse).filter_by(assessment_id=id).delete()

    correct_count = 0
    total_count = 0

    for q_id_str, student_ans in answers_map.items():
        try:
            q_id = int(q_id_str)
        except (ValueError, TypeError):
            continue

        question = db.query(Question).filter_by(id=q_id).first()
        if not question:
            continue

        total_count += 1
        is_correct = (str(student_ans).strip().upper() == str(question.correct_answer).strip().upper())
        if is_correct:
            correct_count += 1

        db.add(AssessmentResponse(
            assessment_id=id,
            question_id=q_id,
            student_answer=str(student_ans),
            is_correct=is_correct,
            created_at=datetime.now(timezone.utc)
        ))

    score_pct = (correct_count / total_count * 100.0) if total_count > 0 else 0.0
    assessment.score = score_pct
    assessment.status = "completed"
    assessment.completed_at = datetime.now(timezone.utc)
    db.commit()

    # Re-run gap detection
    analyze_assessment(db, id, user.id)

    # Re-generate learning path with updated mastery
    generate_personalized_learning_path(db, user.id)

    # Compute Before vs After Comparison
    updated_masteries = db.query(ConceptMastery).filter_by(student_id=user.id).all()
    comparison = []
    total_diff = 0.0

    for m in updated_masteries:
        concept = db.query(Concept).filter_by(id=m.concept_id).first()
        if not concept:
            continue
        prev = previous_mastery.get(m.concept_id, {"score": 0.0, "status": "needs_attention"})
        diff = round(m.score - prev["score"], 1)
        total_diff += diff
        
        comparison.append({
            "concept_id": concept.id,
            "concept_name": concept.name,
            "before_score": round(prev["score"], 1),
            "after_score": round(m.score, 1),
            "before_status": prev["status"],
            "after_status": m.status,
            "improved": (m.score > prev["score"]),
            "score_diff": diff
        })

    return {
        "assessment_id": assessment.id,
        "score": round(score_pct, 1),
        "comparison": comparison,
        "overall_improvement": round(total_diff / len(comparison), 1) if comparison else 0.0
    }
