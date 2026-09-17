import json
from sqlalchemy.orm import Session
from ..models.user import User
from ..models.concept import Subject, Concept, ConceptPrerequisite
from ..models.question import Question, QuestionOption
from ..models.learning import LearningResource
from ..models.teacher_student import TeacherStudent
from ..middleware.auth import get_password_hash
from .data import SUBJECTS, CONCEPTS, PREREQUISITES, QUESTIONS, LEARNING_RESOURCES

def seed_database(db: Session):
    # Ensure subjects exist
    if db.query(Subject).count() == 0:
        for s_data in SUBJECTS:
            s = Subject(name=s_data["name"], description=s_data["description"])
            db.add(s)
        db.commit()

    subject = db.query(Subject).filter_by(name="Mathematics").first()
    if not subject:
        return

    # Seed concepts
    concept_map = {}
    for c in CONCEPTS:
        existing = db.query(Concept).filter_by(name=c["name"]).first()
        if not existing:
            existing = Concept(
                subject_id=subject.id,
                name=c["name"],
                description=c["description"],
                difficulty=c["difficulty"],
                grade=c["grade"]
            )
            db.add(existing)
            db.commit()
            db.refresh(existing)
        concept_map[c["name"]] = existing.id

    # Seed prerequisites
    for target_name, prereq_name in PREREQUISITES:
        if target_name in concept_map and prereq_name in concept_map:
            t_id = concept_map[target_name]
            p_id = concept_map[prereq_name]
            existing_p = db.query(ConceptPrerequisite).filter_by(concept_id=t_id, prerequisite_id=p_id).first()
            if not existing_p:
                prereq = ConceptPrerequisite(concept_id=t_id, prerequisite_id=p_id)
                db.add(prereq)
    db.commit()

    # Seed questions and options
    for q_data in QUESTIONS:
        c_id = concept_map.get(q_data["concept_name"])
        if not c_id:
            continue
        existing_q = db.query(Question).filter_by(text=q_data["text"]).first()
        if not existing_q:
            q = Question(
                concept_id=c_id,
                question_type=q_data["question_type"],
                difficulty=q_data["difficulty"],
                text=q_data["text"],
                correct_answer=q_data["correct_answer"],
                explanation=q_data["explanation"]
            )
            db.add(q)
            db.commit()
            db.refresh(q)

            for opt in q_data["options"]:
                qo = QuestionOption(
                    question_id=q.id,
                    option_label=opt["label"],
                    option_text=opt["text"],
                    is_correct=opt["is_correct"]
                )
                db.add(qo)
            db.commit()

    # Seed learning resources
    for c_name, resources in LEARNING_RESOURCES.items():
        c_id = concept_map.get(c_name)
        if not c_id:
            continue
        
        # 1. Explanation
        if not db.query(LearningResource).filter_by(concept_id=c_id, resource_type="explanation").first():
            db.add(LearningResource(
                concept_id=c_id,
                resource_type="explanation",
                title=f"Core Concept: {c_name}",
                content=resources["explanation"]
            ))
        
        # 2. Key Ideas
        if not db.query(LearningResource).filter_by(concept_id=c_id, resource_type="key_ideas").first():
            db.add(LearningResource(
                concept_id=c_id,
                resource_type="key_ideas",
                title=f"Key Ideas & Formulas for {c_name}",
                content=json.dumps(resources["key_ideas"])
            ))

        # 3. Worked Example
        if not db.query(LearningResource).filter_by(concept_id=c_id, resource_type="worked_example").first():
            db.add(LearningResource(
                concept_id=c_id,
                resource_type="worked_example",
                title=f"Step-by-Step Worked Example: {c_name}",
                content=resources["worked_example"]
            ))

        # 4. Common Mistakes
        if not db.query(LearningResource).filter_by(concept_id=c_id, resource_type="common_mistakes").first():
            db.add(LearningResource(
                concept_id=c_id,
                resource_type="common_mistakes",
                title=f"Common Pitfalls & Mistakes in {c_name}",
                content=json.dumps(resources["common_mistakes"])
            ))
    db.commit()

    # Seed demo accounts
    student = db.query(User).filter_by(email="student@gapwise.ai").first()
    if not student:
        student = User(
            name="Demo Student",
            email="student@gapwise.ai",
            hashed_password=get_password_hash("demo123"),
            role="student"
        )
        db.add(student)
        db.commit()
        db.refresh(student)

    teacher = db.query(User).filter_by(email="teacher@gapwise.ai").first()
    if not teacher:
        teacher = User(
            name="Demo Teacher",
            email="teacher@gapwise.ai",
            hashed_password=get_password_hash("demo123"),
            role="teacher"
        )
        db.add(teacher)
        db.commit()
        db.refresh(teacher)

    ts = db.query(TeacherStudent).filter_by(teacher_id=teacher.id, student_id=student.id).first()
    if not ts:
        ts = TeacherStudent(teacher_id=teacher.id, student_id=student.id)
        db.add(ts)
        db.commit()

    # Seed demo classroom
    from ..models.classroom import Classroom, ClassroomStudent
    demo_class = db.query(Classroom).filter_by(class_code="DEMO10A").first()
    if not demo_class:
        demo_class = Classroom(
            teacher_id=teacher.id,
            name="Class 10-A Mathematics",
            grade="Class 10",
            subject="Mathematics",
            class_code="DEMO10A",
            description="Official Class 10 Section A Mathematics learning group for SIH 2026."
        )
        db.add(demo_class)
        db.commit()
        db.refresh(demo_class)

    cs = db.query(ClassroomStudent).filter_by(classroom_id=demo_class.id, student_id=student.id).first()
    if not cs:
        cs = ClassroomStudent(classroom_id=demo_class.id, student_id=student.id)
        db.add(cs)
        db.commit()

