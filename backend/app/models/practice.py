from datetime import datetime, timezone
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base

class PracticeAttempt(Base):
    __tablename__ = "practice_attempts"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    concept_id: Mapped[int] = mapped_column(ForeignKey("concepts.id"))
    answer: Mapped[str]
    is_correct: Mapped[bool]
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
