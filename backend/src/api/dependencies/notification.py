from typing import Annotated, Callable, Awaitable, Optional

from fastapi import Depends, Query

from src.api.dependencies.db import DBSession
from src.services import NotificationService
from src.repositories import NotificationRepository, UserRepository
from src.schemas.notification import NotificationBody, LatestNotificationsPublic, NotificationPublic
from src.utils.dependency_factory import DependencyFactory
from src.api.websockets.notification import ws_notification_manager


async def service_dep(session: DBSession) -> NotificationService:
    return NotificationService(
        session=session,
        notification_repo=NotificationRepository,
        user_repo=UserRepository)
    
    
async def alert_func(data):
    id = int(data.get('id'))
    await ws_notification_manager.broadcast(id, data)


class NotificationDependencyFactory(DependencyFactory):
    def __init__(self):
        super().__init__(
            service_dep=service_dep,
            SchemaBody=NotificationBody,
            SchemaPublic=NotificationPublic,
            alert_func=alert_func
        )
        
    def get_latest_notifications_dep(self) -> Callable[[], Awaitable[LatestNotificationsPublic]]:
        async def dep(
            service: NotificationService = Depends(self.service_dep),
            userId: Optional[int] = Query(None, examples=[1])) -> LatestNotificationsPublic:
            d = await service.get_latest(userId)
            data = [
                NotificationPublic.model_validate(notification, from_attributes=True)
                for notification in d
            ]
            response = LatestNotificationsPublic(data=data)
            return response
        return dep
    
    
dependencies = NotificationDependencyFactory()


CreatedNotification = Annotated[NotificationPublic, Depends(dependencies.create_dep())]

LatestNotifications = Annotated[LatestNotificationsPublic, Depends(dependencies.get_latest_notifications_dep())]
