from src.utils.repository import SQLAlchemyRepository
from src.models import Notification


class NotificationRepository(SQLAlchemyRepository):
    model = Notification
