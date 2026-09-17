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
from ..services.prerequisite_engine import find_root_causes
from ..services.learning_path import generate_personalized_learning_path

router = APIRouter(prefix="/api/assessment", tags=["assessment"])

@router.post("/start")
def start_assessment(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("student"))
):
    # Create new assessment session
    assessment = Assessment(
        student_id=user.id,
        assessment_type="diagnostic",
        status="in_progress",
        created_at=datetime.now(timezone.utc)
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    # Fetch curated questions across concepts
    questions = db.query(Question).all()
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
def submit_assessment(
    id: int,
    payload: dict = Body(...),
    db: Session = Depends(get_db),
    user: User = Depends(require_role("student"))
):
    assessment = db.query(Assessment).filter_by(id=id, student_id=user.id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    answers_map = {}
    if "answers" in payload:
        answers_map = payload["answers"]
    elif "responses" in payload:
        for item in payload["responses"]:
            answers_map[item.get("question_id")] = item.get("answer")

    db.query(AssessmentResponse).filter_by(assessment_id=id).delete()

    correct_count = 0
    total_count = 0
    questions_review = []
    incorrect_questions = []

    # Get all questions ordered so question numbers are deterministic
    all_questions = db.query(Question).order_by(Question.id.asc()).all()
    q_num_counter = 1

    for question in all_questions:
        if str(question.id) in answers_map or question.id in answers_map:
            student_ans = answers_map.get(str(question.id), answers_map.get(question.id))
            total_count += 1
            is_correct = (str(student_ans).strip().upper() == str(question.correct_answer).strip().upper())
            if is_correct:
                correct_count += 1

            db.add(AssessmentResponse(
                assessment_id=id,
                question_id=question.id,
                student_answer=str(student_ans),
                is_correct=is_correct,
                created_at=datetime.now(timezone.utc)
            ))

            concept = db.query(Concept).filter_by(id=question.concept_id).first()
            options = db.query(QuestionOption).filter_by(question_id=question.id).order_by(QuestionOption.option_label).all()
            
            q_info = {
                "question_num": q_num_counter,
                "question_id": question.id,
                "text": question.text,
                "concept_id": question.concept_id,
                "concept_name": concept.name if concept else "Mathematics",
                "difficulty": question.difficulty,
                "student_answer": str(student_ans),
                "correct_answer": question.correct_answer,
                "is_correct": is_correct,
                "explanation": question.explanation,
                "options": [
                    {
                        "id": opt.id,
                        "label": opt.option_label,
                        "text": opt.option_text,
                        "is_correct": opt.option_label == question.correct_answer
                    }
                    for opt in options
                ]
            }
            questions_review.append(q_info)
            if not is_correct:
                incorrect_questions.append(q_info)

            q_num_counter += 1

    score_pct = (correct_count / total_count * 100.0) if total_count > 0 else 0.0
    assessment.score = score_pct
    assessment.status = "completed"
    assessment.completed_at = datetime.now(timezone.utc)
    db.commit()

    # Run gap detection AI
    concept_results = analyze_assessment(db, id, user.id)

    # Run root cause analysis
    weak_ids = [c["concept_id"] for c in concept_results if c["status"] in ["needs_attention", "developing"]]
    root_causes = find_root_causes(db, user.id, weak_ids)

    # Generate personalized learning path
    generate_personalized_learning_path(db, user.id)

    return {
        "id": assessment.id,
        "score": round(score_pct, 1),
        "date": assessment.completed_at.isoformat(),
        "total_questions": total_count,
        "correct_answers": correct_count,
        "incorrect_count": len(incorrect_questions),
        "concepts": concept_results,
        "concept_mastery": concept_results,
        "rootCauses": root_causes,
        "root_cause_analysis": root_causes,
        "questions_review": questions_review,
        "incorrect_questions": incorrect_questions,
        "learning_path_generated": True
    }

@router.get("/{id}/report")
def get_report(
    id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("student"))
):
    assessment = db.query(Assessment).filter_by(id=id, student_id=user.id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment report not found")

    # Fetch mastery
    masteries = db.query(ConceptMastery).filter_by(student_id=user.id).all()
    concept_results = []
    weak_ids = []

    for m in masteries:
        concept = db.query(Concept).filter_by(id=m.concept_id).first()
        if concept:
            concept_results.append({
                "id": concept.id,
                "concept_id": concept.id,
                "name": concept.name,
                "score": round(m.score, 1),
                "status": m.status
            })
            if m.status in ["needs_attention", "developing"]:
                weak_ids.append(concept.id)

    root_causes = find_root_causes(db, user.id, weak_ids)

    # Build question-by-question review
    responses = db.query(AssessmentResponse).filter_by(assessment_id=id).order_by(AssessmentResponse.id.asc()).all()
    questions_review = []
    incorrect_questions = []

    for idx, resp in enumerate(responses):
        question = db.query(Question).filter_by(id=resp.question_id).first()
        if not question:
            continue
        concept = db.query(Concept).filter_by(id=question.concept_id).first()
        options = db.query(QuestionOption).filter_by(question_id=question.id).order_by(QuestionOption.option_label).all()

        q_info = {
            "question_num": idx + 1,
            "question_id": question.id,
            "text": question.text,
            "concept_id": question.concept_id,
            "concept_name": concept.name if concept else "Mathematics",
            "difficulty": question.difficulty,
            "student_answer": resp.student_answer,
            "correct_answer": question.correct_answer,
            "is_correct": resp.is_correct,
            "explanation": question.explanation,
            "options": [
                {
                    "id": opt.id,
                    "label": opt.option_label,
                    "text": opt.option_text,
                    "is_correct": opt.option_label == question.correct_answer
                }
                for opt in options
            ]
        }
        questions_review.append(q_info)
        if not resp.is_correct:
            incorrect_questions.append(q_info)

    return {
        "id": assessment.id,
        "score": round(assessment.score or 0.0, 1),
        "date": (assessment.completed_at or assessment.created_at).isoformat(),
        "total_questions": len(responses),
        "correct_answers": sum(1 for r in responses if r.is_correct),
        "incorrect_count": len(incorrect_questions),
        "concepts": concept_results,
        "rootCauses": root_causes,
        "root_cause_analysis": root_causes,
        "questions_review": questions_review,
        "incorrect_questions": incorrect_questions
    }

@router.get("/history")
def get_history(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("student"))
):
    assessments = db.query(Assessment).filter_by(student_id=user.id).order_by(Assessment.created_at.desc()).all()
    return [
        {
            "id": a.id,
            "type": a.assessment_type,
            "status": a.status,
            "score": round(a.score, 1) if a.score is not None else None,
            "date": (a.completed_at or a.created_at).isoformat()
        }
        for a in assessments
    ]
