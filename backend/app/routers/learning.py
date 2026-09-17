import json
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..models.concept import Concept, ConceptPrerequisite
from ..models.mastery import ConceptMastery
from ..models.learning import LearningPath, LearningPathItem, LearningResource
from ..models.question import Question, QuestionOption
from ..models.practice import PracticeAttempt
from ..middleware.auth import get_current_user, require_role
from ..services.learning_path import generate_personalized_learning_path

router = APIRouter(prefix="/api/learning", tags=["learning"])

@router.get("/path")
def get_path(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("student"))
):
    active_path = db.query(LearningPath).filter_by(student_id=user.id, is_active=True).first()
    if not active_path:
        has_mastery = db.query(ConceptMastery).filter_by(student_id=user.id).count() > 0
        if has_mastery:
            path_items = generate_personalized_learning_path(db, user.id)
            return {"path": path_items, "items": path_items}
        return {"path": [], "items": []}

    items = db.query(LearningPathItem).filter_by(path_id=active_path.id).order_by(LearningPathItem.order).all()
    formatted = []
    for item in items:
        concept = db.query(Concept).filter_by(id=item.concept_id).first()
        if concept:
            m = db.query(ConceptMastery).filter_by(student_id=user.id, concept_id=concept.id).first()
            formatted.append({
                "id": concept.id,
                "concept_id": concept.id,
                "name": concept.name,
                "description": concept.description,
                "difficulty": concept.difficulty,
                "grade": concept.grade,
                "status": m.status if m else item.status,
                "score": round(m.score, 1) if m else 0.0,
                "reason": item.reason,
                "locked": item.is_locked,
                "is_locked": item.is_locked,
                "order": item.order
            })
    return {"path": formatted, "items": formatted}

@router.get("/concept/{id}")
def get_concept(
    id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("student"))
):
    concept = db.query(Concept).filter_by(id=id).first()
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")

    resources = db.query(LearningResource).filter_by(concept_id=id).all()
    
    explanation = ""
    key_ideas = []
    worked_example = ""
    common_mistakes = []

    for r in resources:
        if r.resource_type == "explanation":
            explanation = r.content
        elif r.resource_type == "key_ideas":
            try:
                key_ideas = json.loads(r.content)
            except:
                key_ideas = [r.content]
        elif r.resource_type == "worked_example":
            worked_example = r.content
        elif r.resource_type == "common_mistakes":
            try:
                common_mistakes = json.loads(r.content)
            except:
                common_mistakes = [r.content]

    mastery = db.query(ConceptMastery).filter_by(student_id=user.id, concept_id=id).first()

    return {
        "id": concept.id,
        "name": concept.name,
        "description": concept.description,
        "difficulty": concept.difficulty,
        "grade": concept.grade,
        "explanation": explanation,
        "keyIdeas": key_ideas,
        "key_ideas": key_ideas,
        "workedExample": worked_example,
        "worked_example": worked_example,
        "commonMistakes": common_mistakes,
        "common_mistakes": common_mistakes,
        "mastery_score": round(mastery.score, 1) if mastery else 0.0,
        "mastery_status": mastery.status if mastery else "needs_attention"
    }

@router.get("/concept/{id}/practice")
def get_practice_questions(
    id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("student"))
):
    concept = db.query(Concept).filter_by(id=id).first()
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")

    questions = db.query(Question).filter_by(concept_id=id).all()
    results = []
    for q in questions:
        options = db.query(QuestionOption).filter_by(question_id=q.id).order_by(QuestionOption.option_label).all()
        results.append({
            "id": q.id,
            "concept_id": q.concept_id,
            "concept_name": concept.name,
            "text": q.text,
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
    return results

@router.post("/practice/submit")
def submit_practice(
    payload: dict = Body(...),
    db: Session = Depends(get_db),
    user: User = Depends(require_role("student"))
):
    """
    Submits a practice question answer.
    Evaluates answers and updates student's concept mastery score dynamically.
    """
    question_id = payload.get("question_id")
    answer = payload.get("answer")
    concept_id = payload.get("concept_id")

    if question_id:
        question = db.query(Question).filter_by(id=question_id).first()
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        
        cid = question.concept_id
        is_correct = (str(answer).strip().upper() == str(question.correct_answer).strip().upper())

        attempt = PracticeAttempt(
            student_id=user.id,
            question_id=question.id,
            concept_id=cid,
            answer=str(answer),
            is_correct=is_correct,
            created_at=datetime.now(timezone.utc)
        )
        db.add(attempt)
        db.commit()

        # Recalculate concept mastery from all attempts
        all_attempts = db.query(PracticeAttempt).filter_by(student_id=user.id, concept_id=cid).all()
        if all_attempts:
            correct_count = sum(1 for a in all_attempts if a.is_correct)
            new_score = round((correct_count / len(all_attempts)) * 100.0, 1)
        else:
            new_score = 100.0 if is_correct else 0.0

        if new_score >= 75.0:
            new_status = 'mastered'
        elif new_score >= 40.0:
            new_status = 'developing'
        else:
            new_status = 'needs_attention'

        mastery = db.query(ConceptMastery).filter_by(student_id=user.id, concept_id=cid).first()
        if not mastery:
            mastery = ConceptMastery(
                student_id=user.id,
                concept_id=cid,
                score=new_score,
                status=new_status,
                attempts=len(all_attempts),
                last_assessed=datetime.now(timezone.utc)
            )
            db.add(mastery)
        else:
            mastery.score = new_score
            mastery.status = new_status
            mastery.attempts += 1
            mastery.last_assessed = datetime.now(timezone.utc)

        db.commit()

        return {
            "is_correct": is_correct,
            "correct_answer": question.correct_answer,
            "explanation": question.explanation,
            "new_mastery_score": new_score,
            "new_status": new_status
        }

    return {"status": "ok"}
