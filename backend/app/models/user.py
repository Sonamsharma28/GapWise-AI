from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    role: Mapped[str] = mapped_column() # 'student' or 'teacher'
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
