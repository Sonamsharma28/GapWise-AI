from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.auth import RegisterRequest, LoginRequest, AuthResponse
from ..models.user import User
from ..models.classroom import Classroom, ClassroomStudent
from ..models.teacher_student import TeacherStudent
from ..middleware.auth import get_password_hash, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=AuthResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == request.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # If class_code provided for student, validate it first
    target_class = None
    if request.role == "student" and request.class_code:
        code_clean = request.class_code.strip().upper()
        target_class = db.query(Classroom).filter(Classroom.class_code == code_clean).first()
        if not target_class:
            raise HTTPException(status_code=400, detail=f"Class Code '{request.class_code}' not found. Please check with your teacher.")

    user = User(
        name=request.name,
        email=request.email,
        hashed_password=get_password_hash(request.password),
        role=request.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Enroll in classroom if specified
    if target_class:
        db.add(ClassroomStudent(classroom_id=target_class.id, student_id=user.id))
        # Ensure teacher-student relationship exists
        if not db.query(TeacherStudent).filter_by(teacher_id=target_class.teacher_id, student_id=user.id).first():
            db.add(TeacherStudent(teacher_id=target_class.teacher_id, student_id=user.id))
        db.commit()

    token = create_access_token(data={"sub": user.email})
    return {"user": user, "token": token}

@router.post("/login", response_model=AuthResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token(data={"sub": user.email})
    return {"user": user, "token": token}

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/class-lookup/{class_code}")
def lookup_class(class_code: str, db: Session = Depends(get_db)):
    code_clean = class_code.strip().upper()
    classroom = db.query(Classroom).filter(Classroom.class_code == code_clean).first()
    if not classroom:
        raise HTTPException(status_code=404, detail="Class Code not found")
    teacher = db.query(User).filter(User.id == classroom.teacher_id).first()
    return {
        "id": classroom.id,
        "name": classroom.name,
        "grade": classroom.grade,
        "subject": classroom.subject,
        "class_code": classroom.class_code,
        "description": classroom.description,
        "teacher_name": teacher.name if teacher else "Teacher"
    }
