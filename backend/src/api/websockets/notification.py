from typing import Union
import uuid

from src.utils.ws_manager import WSManager


class WSNotification(WSManager):
    WEBSOCKET_PATH = "/ws/notifications"
    
    async def broadcast(self, user_id: Union[int, uuid.UUID], data: dict) -> None:
        d = dict()
        d["type"] = "notification"
        d["shortMessage"] = data.get("shortMessage")
        for websocket in self.active_connections.get(user_id, []):
            await websocket.send_json(d)


ws_notification_manager = WSNotification()
