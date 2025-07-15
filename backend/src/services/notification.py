from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.service import Service
from src.utils.repository import Repository, transaction
from src.schemas.notification import NotificationBody
from src.utils.token import token_worker


class NotificationService(Service):
    def __init__(
        self,
        session: AsyncSession,
        notification_repo: Repository,
        user_repo: Repository
    ):
        super().__init__()
        self.session = session
        self.notification_repo = notification_repo
        self.user_repo = user_repo
        self.single_repo = notification_repo
        self.jwt = token_worker
    
    @transaction
    async def create(self, body: NotificationBody) -> Union[int, str]:
        user = await self.user_repo(self.session).select_one_by_id(body.userId)
        if not user:
            return "User id has not found"
        id = await self.notification_repo(self.session).create_one(**body.model_dump())
        return id 
    
    async def get_latest(self, userId) -> Union[list, str]:
        data = await self.notification_repo(self.session).select_latest(userId=userId)
        return data
