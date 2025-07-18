from sqlalchemy.ext.asyncio import create_async_engine

from src.config import settings


engine = create_async_engine(url=settings.TEST_POSTGRES, echo=True)
