from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.routing import WebSocketRoute

from src.utils.application import Application
from src.databases.pg_manager import sessionmanager
from src.api.tags_metadata import tags_metadata
from src.api.routers import *
from src.api.websockets import *


class API(Application):
    def __init__(self):
        super().__init__()
        self.title = "Notifications"
        self.tags_metadata = tags_metadata
        self.routers = [
            notification_router,
            user_router
        ]
        self.websockets = [
            WebSocketRoute("/ws/pingpong", WSPingPong),
            WebSocketRoute("/ws/notifications", WSNotification)
        ]
    
    @staticmethod
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        sessionmanager.connect_to_db()
        yield
        await sessionmanager.close()

    def create(self):
        self.app = FastAPI(
            title=self.title,
            lifespan=self.lifespan,
            openapi_tags=self.tags_metadata
        )
        for router in self.routers:
            self.app.include_router(router)
        for websocket in self.websockets:
            self.app.router.routes.append(websocket)
        return self.app
    
    def run():
        pass
