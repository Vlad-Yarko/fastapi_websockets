from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class User(Base):
    __tablename__ = "users"
    
    username: Mapped[str] = mapped_column(String(60), nullable=False)
    password: Mapped[bytes] = mapped_column(nullable=False)
