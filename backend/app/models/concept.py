from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base

class Subject(Base):
    __tablename__ = "subjects"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]

class Concept(Base):
    __tablename__ = "concepts"
    id: Mapped[int] = mapped_column(primary_key=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    name: Mapped[str]
    description: Mapped[str] = mapped_column(Text)
    difficulty: Mapped[int]
    grade: Mapped[str]

class ConceptPrerequisite(Base):
    __tablename__ = "concept_prerequisites"
    id: Mapped[int] = mapped_column(primary_key=True)
    concept_id: Mapped[int] = mapped_column(ForeignKey("concepts.id"))
    prerequisite_id: Mapped[int] = mapped_column(ForeignKey("concepts.id"))
