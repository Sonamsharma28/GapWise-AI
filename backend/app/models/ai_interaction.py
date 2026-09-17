from datetime import datetime, timezone
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base

class AIInteraction(Base):
    __tablename__ = "ai_interactions"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    query: Mapped[str] = mapped_column(Text)
    response: Mapped[str] = mapped_column(Text)
    context_concepts: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
