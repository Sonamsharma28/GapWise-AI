from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base

class TeacherStudent(Base):
    __tablename__ = "teacher_students"
    id: Mapped[int] = mapped_column(primary_key=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
