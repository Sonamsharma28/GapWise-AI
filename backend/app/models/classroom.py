from datetime import datetime, timezone
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base

class Classroom(Base):
    __tablename__ = "classrooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(100))
    grade: Mapped[str] = mapped_column(String(50), default="Class 10")
    subject: Mapped[str] = mapped_column(String(100), default="Mathematics")
    class_code: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, default=None)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

class ClassroomStudent(Base):
    __tablename__ = "classroom_students"

    id: Mapped[int] = mapped_column(primary_key=True)
    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id"))
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    joined_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
