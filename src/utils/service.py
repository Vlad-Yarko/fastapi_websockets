from typing import Optional, Union
import uuid

from src.databases import redis_manager
from src.utils.token import token_worker


class Service:
    def __init__(self):
        self.pagination_repo = None
        self.single_repo = None
        self.redis_manager = redis_manager
        self.jwt = token_worker
    
    async def get_with_pagination(self, page: Optional[int], **kwargs) -> Optional[dict]:
        full_data = await self.pagination_repo(self.session).select_all(page, **kwargs)
        data, total, offset = full_data
        count = len(data)
        next = False
        if page is not None:
            next = (page * offset) < total
        res = {
            "data": data,
            "page": page,
            "count": count,
            "total": total,
            "hasNext": next
        }
        return res
    
    async def get(self, id: int):
        data = await self.single_repo(self.session).select_by_id(id)
        return data
    
    async def validate_token(self, token: str) -> Union[str, uuid.UUID, int]:
        id = self.jwt.validate_token(token)
        if id is None:
            return "Bearer token is missing"
        try:
            user = await self.user_repo(self.session).select_one_by_id(int(id))
        except Exception:
            user = None
        if not user:
            return "Invalid token"
        return user
    
    async def issue_refresh_token(self, id: int, exp: Optional[int] = None) -> str:
        token = self.jwt.create_refresh_token(id, exp)
        return token
    
    async def issue_access_token(self, id: int) -> str:
        token = self.jwt.create_access_token(id)
        return token
