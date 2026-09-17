from datetime import datetime, timezone
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base

class ConceptMastery(Base):
    __tablename__ = "concept_masteries"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    concept_id: Mapped[int] = mapped_column(ForeignKey("concepts.id"))
    score: Mapped[float]
    status: Mapped[str]
    attempts: Mapped[int] = mapped_column(default=0)
    last_assessed: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    
    __table_args__ = (
        UniqueConstraint('student_id', 'concept_id', name='uq_student_concept_mastery'),
    )
