from typing import Optional, Union
import uuid

from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.service import Service
from src.utils.repository import Repository, transaction
from src.utils.password import pw_worker
from src.utils.token import token_worker
from src.schemas.user import UserBody, UserPublic
from src.models import User 
from src.enums.user import TokenEnum


class UserService(Service):
    def __init__(
        self,
        session: AsyncSession,
        user_repo: Repository
    ):
        super().__init__()
        self.session = session
        self.user_repo = user_repo
        self.jwt = token_worker
        self.pw = pw_worker
        self.single_repo = user_repo
        
    async def get_user(self, username: str) -> Optional[User]:
        user = await self.user_repo(self.session).select_user_by_username(username)
        return user
    
    @transaction
    async def create(self, body: UserBody) -> Union[int, str]:
        user = await self.get_user(body.username)
        if user:
            return "Username has already found"
        password = pw_worker.hash_password(body.password)
        user_id = await self.user_repo(self.session).create_one(username=body.username, password=password)
        return user_id
    
    async def login(self, body: UserBody) -> Union[dict, str]:
        user = await self.get_user(body.username)
        if not user:
            return "Username has not found"
        is_correct_pw = self.pw.check_password(body.password, user.password)
        if not is_correct_pw:
            return "Incorrect password"
        refresh_token = await self.issue_refresh_token(str(user.id))
        data = dict()
        token_id = str(uuid.uuid4())
        data["id"] = user.id
        data["username"] = user.username
        data["tokenId"] = token_id
        await self.redis_manager.set_string_data(f"{token_id}:{user.id}", refresh_token, TokenEnum.REFRESH_TOKEN_EXP.value)
        # access_token = await self.issue_access_token(user.id)
        return data
    
    async def issue_token(
        self, 
        token_id: Union[str, uuid.UUID],
        user_id: int) -> Union[tuple[str, int], str]:
        full_id = f"{token_id}:{user_id}"
        token = await self.redis_manager.get_string_data(full_id)
        if not token:
            return "Token id or user id has not found", status.HTTP_400_BAD_REQUEST
        payload = await self.jwt.validate_token(token)
        if not payload:
            return "User is not authenticated. Refresh token has not found", status.HTTP_401_UNAUTHORIZED
        if payload["sub"] != str(user_id):
            return "User id is invalid", status.HTTP_422_UNPROCESSABLE_ENTITY,
        token_id = str(uuid.uuid4())
        expiration_time = payload.get('exp')
        await self.redis_manager.delete(full_id)
        await self.redis_manager.set_string_data(f"{token_id}:{user_id}", token, expiration_time)
        access_token = await self.issue_access_token(user_id)
        data = {
            "accessToken": access_token,
            "exp": expiration_time,
            "tokenId": token_id
        }
        return data
