from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..models.assessment import Assessment, AssessmentResponse
from ..models.question import Question, QuestionOption
from ..models.concept import Concept
from ..models.mastery import ConceptMastery
from ..models.learning import LearningPath, LearningPathItem
from ..models.classroom import Classroom, ClassroomStudent
from ..models.teacher_student import TeacherStudent
from ..schemas.classroom import JoinClassRequest
from ..middleware.auth import get_current_user, require_role
from ..services.prerequisite_engine import find_root_causes

router = APIRouter(prefix="/api/student", tags=["student"])

@router.get("/dashboard")
def get_dashboard(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("student"))
):
    # Check if student is enrolled in a classroom
    cs_entry = db.query(ClassroomStudent).filter_by(student_id=user.id).first()
    enrolled_class = None
    if cs_entry:
        c_obj = db.query(Classroom).filter_by(id=cs_entry.classroom_id).first()
        if c_obj:
            t_user = db.query(User).filter_by(id=c_obj.teacher_id).first()
            enrolled_class = {
                "id": c_obj.id,
                "name": c_obj.name,
                "grade": c_obj.grade,
                "subject": c_obj.subject,
                "class_code": c_obj.class_code,
                "teacher_name": t_user.name if t_user else "Teacher",
                "joined_at": cs_entry.joined_at.strftime("%b %d, %Y")
            }

    # Check if student completed any assessment
    completed_assessments = db.query(Assessment).filter_by(student_id=user.id, status="completed").order_by(Assessment.completed_at.desc()).all()
    has_assessment = len(completed_assessments) > 0

    if not has_assessment:
        return {
            "hasAssessment": False,
            "has_assessment": False,
            "name": user.name,
            "overallMastery": 0.0,
            "counts": {"mastered": 0, "developing": 0, "needs_attention": 0},
            "concepts": [],
            "recommendation": None,
            "recent_incorrect_questions": [],
            "enrolled_class": enrolled_class
        }

    # Fetch mastery records
    masteries = db.query(ConceptMastery).filter_by(student_id=user.id).all()
    
    concepts_data = []
    counts = {"mastered": 0, "developing": 0, "needs_attention": 0}
    total_score = 0.0
    weak_ids = []

    for m in masteries:
        concept = db.query(Concept).filter_by(id=m.concept_id).first()
        if not concept:
            continue
        c_score = round(m.score, 1)
        total_score += c_score
        counts[m.status] = counts.get(m.status, 0) + 1
        
        if m.status in ["needs_attention", "developing"]:
            weak_ids.append(concept.id)

        concepts_data.append({
            "id": concept.id,
            "concept_id": concept.id,
            "name": concept.name,
            "score": c_score,
            "status": m.status,
            "difficulty": concept.difficulty
        })

    overall_mastery = round(total_score / len(masteries), 1) if masteries else 0.0

    # Build smart recommendation
    root_causes = find_root_causes(db, user.id, weak_ids) if weak_ids else []
    if root_causes:
        top_rc = root_causes[0]
        rec_message = f"Focus on mastering '{top_rc['prerequisiteConcept']}' first to overcome hurdles in '{top_rc['targetConcept']}'."
        rec_target = top_rc['prerequisiteConcept']
    elif weak_ids:
        weak_c = db.query(Concept).filter_by(id=weak_ids[0]).first()
        rec_message = f"Continue targeted practice in '{weak_c.name}' to reach full mastery."
        rec_target = weak_c.name
    else:
        rec_message = "Outstanding progress! You have mastered foundational Class 9-10 Mathematics concepts."
        rec_target = "Complete Mastery"

    recent_a = completed_assessments[0]
    recent_info = {
        "id": recent_a.id,
        "score": round(recent_a.score or 0.0, 1),
        "date": (recent_a.completed_at or recent_a.created_at).isoformat()
    }

    # Fetch incorrect questions from latest assessment
    latest_responses = db.query(AssessmentResponse).filter_by(assessment_id=recent_a.id).order_by(AssessmentResponse.id.asc()).all()
    recent_incorrect_questions = []

    for idx, resp in enumerate(latest_responses):
        if not resp.is_correct:
            q = db.query(Question).filter_by(id=resp.question_id).first()
            if q:
                c = db.query(Concept).filter_by(id=q.concept_id).first()
                opts = db.query(QuestionOption).filter_by(question_id=q.id).order_by(QuestionOption.option_label).all()
                recent_incorrect_questions.append({
                    "question_num": idx + 1,
                    "question_id": q.id,
                    "text": q.text,
                    "concept_id": q.concept_id,
                    "concept_name": c.name if c else "Mathematics",
                    "difficulty": q.difficulty,
                    "student_answer": resp.student_answer,
                    "correct_answer": q.correct_answer,
                    "explanation": q.explanation,
                    "options": [
                        {
                            "id": opt.id,
                            "label": opt.option_label,
                            "text": opt.option_text,
                            "is_correct": opt.option_label == q.correct_answer
                        }
                        for opt in opts
                    ]
                })

    return {
        "hasAssessment": True,
        "has_assessment": True,
        "name": user.name,
        "overallMastery": overall_mastery,
        "overall_mastery": overall_mastery,
        "counts": counts,
        "concepts": concepts_data,
        "recommendation": {
            "message": rec_message,
            "target": rec_target
        },
        "recentAssessment": recent_info,
        "recent_incorrect_questions": recent_incorrect_questions,
        "incorrect_count": len(recent_incorrect_questions),
        "enrolled_class": enrolled_class
    }

@router.post("/join-class")
def join_class(
    request: JoinClassRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("student"))
):
    code_clean = request.class_code.strip().upper()
    classroom = db.query(Classroom).filter_by(class_code=code_clean).first()
    if not classroom:
        raise HTTPException(status_code=404, detail=f"Class Code '{request.class_code}' not found. Please check with your teacher.")

    # Check if already joined
    existing_cs = db.query(ClassroomStudent).filter_by(classroom_id=classroom.id, student_id=user.id).first()
    if not existing_cs:
        db.add(ClassroomStudent(
            classroom_id=classroom.id,
            student_id=user.id,
            joined_at=datetime.now(timezone.utc)
        ))

    # Link teacher and student
    if not db.query(TeacherStudent).filter_by(teacher_id=classroom.teacher_id, student_id=user.id).first():
        db.add(TeacherStudent(teacher_id=classroom.teacher_id, student_id=user.id))

    db.commit()

    teacher = db.query(User).filter_by(id=classroom.teacher_id).first()
    return {
        "message": f"Successfully joined {classroom.name}!",
        "classroom": {
            "id": classroom.id,
            "name": classroom.name,
            "grade": classroom.grade,
            "subject": classroom.subject,
            "class_code": classroom.class_code,
            "teacher_name": teacher.name if teacher else "Teacher"
        }
    }

@router.get("/class")
def get_student_class(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("student"))
):
    cs = db.query(ClassroomStudent).filter_by(student_id=user.id).first()
    if not cs:
        return {"enrolled": False, "classroom": None}

    cl = db.query(Classroom).filter_by(id=cs.classroom_id).first()
    if not cl:
        return {"enrolled": False, "classroom": None}

    teacher = db.query(User).filter_by(id=cl.teacher_id).first()
    return {
        "enrolled": True,
        "classroom": {
            "id": cl.id,
            "name": cl.name,
            "grade": cl.grade,
            "subject": cl.subject,
            "class_code": cl.class_code,
            "teacher_name": teacher.name if teacher else "Teacher",
            "joined_at": cs.joined_at.strftime("%b %d, %Y")
        }
    }

@router.get("/mastery")
def get_mastery(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("student"))
):
    masteries = db.query(ConceptMastery).filter_by(student_id=user.id).all()
    results = []
    for m in masteries:
        concept = db.query(Concept).filter_by(id=m.concept_id).first()
        if concept:
            results.append({
                "concept_id": concept.id,
                "name": concept.name,
                "score": round(m.score, 1),
                "status": m.status,
                "attempts": m.attempts,
                "last_assessed": m.last_assessed.isoformat()
            })
    return results

@router.get("/progress")
def get_progress(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("student"))
):
    assessments = db.query(Assessment).filter_by(student_id=user.id, status="completed").order_by(Assessment.completed_at.asc()).all()
    
    timeline = []
    for i, a in enumerate(assessments):
        timeline.append({
            "session": f"Session {i+1} ({a.assessment_type.capitalize()})",
            "score": round(a.score or 0.0, 1),
            "date": (a.completed_at or a.created_at).strftime("%b %d, %H:%M")
        })

    masteries = db.query(ConceptMastery).filter_by(student_id=user.id).all()
    concept_breakdown = []
    for m in masteries:
        c = db.query(Concept).filter_by(id=m.concept_id).first()
        if c:
            concept_breakdown.append({
                "name": c.name,
                "score": round(m.score, 1),
                "status": m.status,
                "attempts": m.attempts
            })

    return {
        "timeline": timeline,
        "concept_breakdown": concept_breakdown,
        "total_assessments": len(assessments)
    }
