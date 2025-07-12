from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class Notification(Base):
    __tablename__ = "notifications"
    
    userId: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    shortMessage: Mapped[str] = mapped_column(String(20), nullable=False)
