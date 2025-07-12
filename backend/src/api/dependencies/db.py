from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.databases.pg_manager import get_db_session


DBSession = Annotated[AsyncSession, Depends(get_db_session)]
