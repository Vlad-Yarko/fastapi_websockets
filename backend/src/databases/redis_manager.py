from typing import Union, Optional

from redis import asyncio as aioredis
from fastapi import HTTPException, status


class RedisManager:
    def __init__(
        self, url: 
        Optional[str] = "redis://localhost"):
        self.engine = aioredis.from_url(url)
        
    async def get_string_data(self, key: str) -> Union[None, str, dict, list]:
        data = await self.engine.get(key)
        return data.decode() if data else data
        
    async def set_string_data(self, key: str, data: str, expired: int = 60) -> None:
        await self.engine.set(key, data)
        await self.engine.expire(key, expired)
        
    async def ttl(self, key: str) -> int:
        time = await self.engine.ttl(key)
        return time
    
    async def delete(self, key: str) -> None:
        await self.engine.expire(key, 0)


redis_manager = RedisManager()
