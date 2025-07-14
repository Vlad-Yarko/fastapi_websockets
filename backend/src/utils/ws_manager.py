from typing import Union
import uuid
from abc import ABC, abstractmethod
import asyncio

from fastapi import WebSocket, WebSocketDisconnect
from starlette.endpoints import WebSocketEndpoint

from src.utils.conn_manager import connection_manager
from src.utils.dependency_factory import WSToken


class WSManager(ABC, WebSocketEndpoint):
    encoding = "json"
    WEBSOCKET_PATH = None

    async def on_connect(self, websocket: WebSocket, user: WSToken) -> None:
        await websocket.accept()
        connection_manager.active_connections[user.id].add(websocket)
        connection_manager.active_tasks[websocket] = (asyncio.create_task(self.ping_loop(websocket, user.id)))
        connection_manager.websocket_to_user_id[websocket] = user.id

    async def on_disconnect(self, websocket: WebSocket) -> None:
        try:
            user_id = connection_manager.websocket_to_user_id[websocket]
            del connection_manager.websocket_to_user_id[websocket]
            connection_manager.active_connections[user_id].discard(websocket)
            task = connection_manager.active_tasks[websocket]
            task.cancel()
            connection_manager.active_tasks[websocket].discard(task)
        except asyncio.CancelledError:
            pass
        except KeyError:
            return
        if not connection_manager.active_connections[user_id]:
            del connection_manager.active_connections[user_id]

    async def on_receive(self, websocket: WebSocket, data):
        if data.get("type") == "ping":
            pass
    
    async def ping_loop(self, websocket: WebSocket, user_id: Union[int, uuid.UUID]):
        # try:
            while True:
                await websocket.send_json({'type': 'ping'})
                asyncio.sleep(10)
        # except WebSocketDisconnect:
        #     await self  

    @abstractmethod
    async def broadcast(self):
        raise NotImplementedError
