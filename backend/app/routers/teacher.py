import random
import string
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..models.assessment import Assessment
from ..models.concept import Concept
from ..models.mastery import ConceptMastery
from ..models.teacher_student import TeacherStudent
from ..models.classroom import Classroom, ClassroomStudent
from ..schemas.classroom import CreateClassRequest, ClassroomResponse
from ..middleware.auth import get_current_user, require_role
from ..services.prerequisite_engine import find_root_causes

router = APIRouter(prefix="/api/teacher", tags=["teacher"])

def generate_random_class_code(length: int = 6) -> str:
    """Generate a clean, uppercase alphanumeric class code (e.g. MATH9A, GAP7X2)."""
    chars = string.ascii_uppercase + string.digits
    # Avoid ambiguous characters like 0, O, 1, I
    clean_chars = ''.join(c for c in chars if c not in '01IO')
    return ''.join(random.choices(clean_chars, k=length))

@router.get("/dashboard")
def get_teacher_dashboard(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    # Fetch classrooms owned by this teacher
    classrooms = db.query(Classroom).filter_by(teacher_id=user.id).order_by(Classroom.created_at.desc()).all()
    
    # Fetch all students linked to this teacher (or enrolled in their classes)
    class_ids = [c.id for c in classrooms]
    enrolled_student_ids = [
        cs.student_id for cs in db.query(ClassroomStudent).filter(ClassroomStudent.classroom_id.in_(class_ids)).all()
    ] if class_ids else []

    direct_student_ids = [
        ts.student_id for ts in db.query(TeacherStudent).filter_by(teacher_id=user.id).all()
    ]

    all_student_ids = list(set(enrolled_student_ids + direct_student_ids))
    if not all_student_ids:
        # Fallback to all students if this is demo
        students = db.query(User).filter_by(role="student").all()
    else:
        students = db.query(User).filter(User.id.in_(all_student_ids)).all()

    concepts = db.query(Concept).all()
    total_students = len(students)
    student_summaries = []
    total_class_score = 0.0
    students_needing_attention = 0
    total_assessments_taken = 0

    for s in students:
        s_masteries = db.query(ConceptMastery).filter_by(student_id=s.id).all()
        s_assessments = db.query(Assessment).filter_by(student_id=s.id, status="completed").count()
        total_assessments_taken += s_assessments

        if s_masteries:
            avg_score = sum(m.score for m in s_masteries) / len(s_masteries)
            has_weak = any(m.status == "needs_attention" for m in s_masteries)
        else:
            avg_score = 0.0
            has_weak = True

        total_class_score += avg_score
        status_label = "Needs Support" if (has_weak or avg_score < 60) else "On Track"
        if status_label == "Needs Support":
            students_needing_attention += 1

        # Check which class this student belongs to
        cs_entry = db.query(ClassroomStudent).filter_by(student_id=s.id).first()
        c_name = None
        if cs_entry:
            c_obj = db.query(Classroom).filter_by(id=cs_entry.classroom_id).first()
            if c_obj:
                c_name = c_obj.name

        student_summaries.append({
            "id": s.id,
            "name": s.name,
            "email": s.email,
            "overallMastery": round(avg_score, 1),
            "status": status_label,
            "classroom": c_name or "Independent Student"
        })

    avg_class_mastery = round(total_class_score / total_students, 1) if total_students > 0 else 0.0

    # Calculate concept-level performance
    concept_performance = []
    for c in concepts:
        c_masteries = db.query(ConceptMastery).filter_by(concept_id=c.id).all()
        if c_masteries:
            c_avg = sum(m.score for m in c_masteries) / len(c_masteries)
            struggling_count = sum(1 for m in c_masteries if m.status == "needs_attention")
        else:
            c_avg = 0.0
            struggling_count = 0

        concept_performance.append({
            "id": c.id,
            "name": c.name,
            "avgScore": round(c_avg, 1),
            "struggling": struggling_count
        })

    # Classrooms list summary
    classroom_summaries = []
    for cl in classrooms:
        cs_list = db.query(ClassroomStudent).filter_by(classroom_id=cl.id).all()
        cl_student_ids = [item.student_id for item in cs_list]
        cl_masteries = db.query(ConceptMastery).filter(ConceptMastery.student_id.in_(cl_student_ids)).all() if cl_student_ids else []
        cl_avg = (sum(m.score for m in cl_masteries) / len(cl_masteries)) if cl_masteries else 0.0

        classroom_summaries.append({
            "id": cl.id,
            "name": cl.name,
            "grade": cl.grade,
            "subject": cl.subject,
            "class_code": cl.class_code,
            "description": cl.description,
            "student_count": len(cs_list),
            "avg_mastery": round(cl_avg, 1),
            "created_at": cl.created_at.strftime("%b %d, %Y")
        })

    return {
        "stats": {
            "totalStudents": total_students,
            "totalClasses": len(classrooms),
            "avgMastery": avg_class_mastery,
            "needsAttention": students_needing_attention,
            "assessmentsTaken": total_assessments_taken
        },
        "classrooms": classroom_summaries,
        "conceptPerformance": concept_performance,
        "students": student_summaries
    }

@router.post("/classes")
def create_class(
    request: CreateClassRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    # Determine unique class code
    if request.class_code and request.class_code.strip():
        code = request.class_code.strip().upper()
        if db.query(Classroom).filter_by(class_code=code).first():
            raise HTTPException(status_code=400, detail=f"Class Code '{code}' is already in use. Please choose another.")
    else:
        # Auto-generate unique code
        prefix = ''.join(w[0] for w in request.name.split() if w.isalnum())[:3].upper()
        if not prefix:
            prefix = "CLS"
        for _ in range(10):
            code = f"{prefix}{generate_random_class_code(4)}"
            if not db.query(Classroom).filter_by(class_code=code).first():
                break

    classroom = Classroom(
        teacher_id=user.id,
        name=request.name.strip(),
        grade=request.grade.strip(),
        subject=request.subject.strip(),
        class_code=code,
        description=request.description.strip() if request.description else None,
        created_at=datetime.now(timezone.utc)
    )
    db.add(classroom)
    db.commit()
    db.refresh(classroom)

    return {
        "id": classroom.id,
        "name": classroom.name,
        "grade": classroom.grade,
        "subject": classroom.subject,
        "class_code": classroom.class_code,
        "description": classroom.description,
        "teacher_name": user.name,
        "student_count": 0,
        "avg_mastery": 0.0,
        "created_at": classroom.created_at.strftime("%b %d, %Y"),
        "share_link": f"/join/{classroom.class_code}"
    }

@router.get("/classes")
def get_teacher_classes(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    classrooms = db.query(Classroom).filter_by(teacher_id=user.id).order_by(Classroom.created_at.desc()).all()
    results = []
    for cl in classrooms:
        cs_list = db.query(ClassroomStudent).filter_by(classroom_id=cl.id).all()
        cl_student_ids = [item.student_id for item in cs_list]
        cl_masteries = db.query(ConceptMastery).filter(ConceptMastery.student_id.in_(cl_student_ids)).all() if cl_student_ids else []
        cl_avg = (sum(m.score for m in cl_masteries) / len(cl_masteries)) if cl_masteries else 0.0

        results.append({
            "id": cl.id,
            "name": cl.name,
            "grade": cl.grade,
            "subject": cl.subject,
            "class_code": cl.class_code,
            "description": cl.description,
            "teacher_name": user.name,
            "student_count": len(cs_list),
            "avg_mastery": round(cl_avg, 1),
            "created_at": cl.created_at.strftime("%b %d, %Y"),
            "share_link": f"/join/{cl.class_code}"
        })
    return results

@router.get("/classes/{class_id}")
def get_class_detail(
    class_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    classroom = db.query(Classroom).filter_by(id=class_id, teacher_id=user.id).first()
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")

    cs_list = db.query(ClassroomStudent).filter_by(classroom_id=classroom.id).all()
    students_data = []

    for cs in cs_list:
        s = db.query(User).filter_by(id=cs.student_id).first()
        if not s:
            continue
        s_masteries = db.query(ConceptMastery).filter_by(student_id=s.id).all()
        avg_score = (sum(m.score for m in s_masteries) / len(s_masteries)) if s_masteries else 0.0
        has_weak = any(m.status == "needs_attention" for m in s_masteries)

        students_data.append({
            "id": s.id,
            "name": s.name,
            "email": s.email,
            "overall_mastery": round(avg_score, 1),
            "status": "Needs Support" if (has_weak or avg_score < 60) else "On Track",
            "joined_at": cs.joined_at.strftime("%b %d, %Y")
        })

    return {
        "id": classroom.id,
        "name": classroom.name,
        "grade": classroom.grade,
        "subject": classroom.subject,
        "class_code": classroom.class_code,
        "description": classroom.description,
        "student_count": len(students_data),
        "students": students_data
    }

@router.get("/students")
def get_all_students(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    students = db.query(User).filter_by(role="student").all()
    results = []
    for s in students:
        s_masteries = db.query(ConceptMastery).filter_by(student_id=s.id).all()
        avg_score = sum(m.score for m in s_masteries) / len(s_masteries) if s_masteries else 0.0
        results.append({
            "id": s.id,
            "name": s.name,
            "email": s.email,
            "overallMastery": round(avg_score, 1)
        })
    return results

@router.get("/student/{id}")
def get_student_detail(
    id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("teacher"))
):
    student = db.query(User).filter_by(id=id, role="student").first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    masteries = db.query(ConceptMastery).filter_by(student_id=student.id).all()
    concepts_data = []
    weak_ids = []
    total_score = 0.0

    for m in masteries:
        concept = db.query(Concept).filter_by(id=m.concept_id).first()
        if concept:
            total_score += m.score
            if m.status in ["needs_attention", "developing"]:
                weak_ids.append(concept.id)
            concepts_data.append({
                "id": concept.id,
                "name": concept.name,
                "score": round(m.score, 1),
                "status": m.status
            })

    overall_mastery = round(total_score / len(masteries), 1) if masteries else 0.0
    root_causes = find_root_causes(db, student.id, weak_ids) if weak_ids else []

    learning_gaps = [
        {
            "prerequisite": rc["prerequisiteConcept"],
            "target": rc["targetConcept"],
            "explanation": rc["explanation"]
        }
        for rc in root_causes
    ]

    assessments = db.query(Assessment).filter_by(student_id=student.id, status="completed").order_by(Assessment.completed_at.desc()).all()
    a_history = [
        {
            "id": a.id,
            "type": a.assessment_type,
            "score": round(a.score, 1) if a.score is not None else None,
            "date": (a.completed_at or a.created_at).strftime("%b %d, %Y")
        }
        for a in assessments
    ]

    return {
        "id": student.id,
        "name": student.name,
        "email": student.email,
        "overallMastery": overall_mastery,
        "concepts": concepts_data,
        "learningGaps": learning_gaps,
        "assessments": a_history
    }
