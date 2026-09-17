from datetime import datetime, timezone
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base

class Assessment(Base):
    __tablename__ = "assessments"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    assessment_type: Mapped[str]
    status: Mapped[str]
    score: Mapped[float | None]
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    completed_at: Mapped[datetime | None]

class AssessmentResponse(Base):
    __tablename__ = "assessment_responses"
    id: Mapped[int] = mapped_column(primary_key=True)
    assessment_id: Mapped[int] = mapped_column(ForeignKey("assessments.id"))
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    student_answer: Mapped[str | None]
    is_correct: Mapped[bool]
    time_taken: Mapped[int | None]
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
