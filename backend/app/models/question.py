from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base

class Question(Base):
    __tablename__ = "questions"
    id: Mapped[int] = mapped_column(primary_key=True)
    concept_id: Mapped[int] = mapped_column(ForeignKey("concepts.id"))
    question_type: Mapped[str]
    difficulty: Mapped[int]
    text: Mapped[str] = mapped_column(Text)
    correct_answer: Mapped[str]
    explanation: Mapped[str] = mapped_column(Text)

class QuestionOption(Base):
    __tablename__ = "question_options"
    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    option_label: Mapped[str]
    option_text: Mapped[str]
    is_correct: Mapped[bool]
