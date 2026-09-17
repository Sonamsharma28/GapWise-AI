from datetime import datetime, timezone
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base

class LearningPath(Base):
    __tablename__ = "learning_paths"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

class LearningPathItem(Base):
    __tablename__ = "learning_path_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    path_id: Mapped[int] = mapped_column(ForeignKey("learning_paths.id"))
    concept_id: Mapped[int] = mapped_column(ForeignKey("concepts.id"))
    order: Mapped[int]
    status: Mapped[str]
    reason: Mapped[str] = mapped_column(Text)
    is_locked: Mapped[bool] = mapped_column(default=True)

class LearningResource(Base):
    __tablename__ = "learning_resources"
    id: Mapped[int] = mapped_column(primary_key=True)
    concept_id: Mapped[int] = mapped_column(ForeignKey("concepts.id"))
    resource_type: Mapped[str]
    title: Mapped[str]
    content: Mapped[str] = mapped_column(Text)
