from typing import Union
import uuid

from src.utils.conn_manager import connection_manager
from src.utils.ws_manager import WSManager


class NotificationManager(WSManager):
    async def broadcast(self, user_id: Union[int, uuid.UUID], data: dict) -> None:
        d = dict()
        d["id"] = data.get("id")
        d["type"] = "notification"
        d["shortMessage"] = data.get("shortMessage")
        for websocket in connection_manager.active_connections.get(user_id, []):
            await websocket.send_json(d)


notification_manager = NotificationManager()
