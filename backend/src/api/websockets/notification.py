from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.api.managers import notification_manager
from src.api.dependencies.notification import WSToken


router = APIRouter()


@router.websocket("/ws/notifications")
async def notifications_websocket(websocket: WebSocket, user: WSToken):
    connection = await notification_manager.connect(websocket, user)
    if not connection:
        return
    try:
        while True:
            await notification_manager.receive(websocket)
    except WebSocketDisconnect:
        await notification_manager.disconnect(websocket, user)
