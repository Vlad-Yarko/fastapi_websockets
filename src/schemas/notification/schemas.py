from pydantic import Field

from src.utils.schema import Schema


class Notification(Schema):
    userId: int = Field(examples=[1])
    shortMessage: str = Field(examples=['My advertisement'], min_length=2, max_length=20)


class NotificationBody(Notification):
    pass


class NotificationPublic(Notification):
    id: int = Field(examples=[1])
    
    model_config = {
        "extra": "ignore"
    }


class LatestNotificationsPublic(Schema):
    data: list[NotificationPublic]
