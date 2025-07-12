from typing import Optional

from src.utils.repository import SQLAlchemyRepository
from src.models import User


class UserRepository(SQLAlchemyRepository):
    model = User
    
    async def select_user_by_username(self, username: str) -> Optional[User]:
        user = await self.select_one("username", username)
        return user
    
    
