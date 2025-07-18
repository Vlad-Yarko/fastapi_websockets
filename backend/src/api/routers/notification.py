from fastapi import APIRouter

from src.schemas.notification import LatestNotificationsPublic, CreateNotification422, NotificationPublic
from src.api.dependencies.notification import LatestNotifications, CreatedNotification


router = APIRouter(
    prefix='/notifications',
    tags=["NOTIFICATION"]
)


@router.get('/latest',
            summary="Gets notifications",
            description="**Gets** latest notifications for **user** (or **all** if userId is not passed)",
            response_model=LatestNotificationsPublic)
async def get_notifications_hand(data: LatestNotifications):
    return data


@router.post('',
            summary="Creates notification",
            description="**Creates** notification for **user**",
            response_model=NotificationPublic,
            responses={
                422: {'model': CreateNotification422}
            })
async def create_notification_hand(data: CreatedNotification):
    return data
