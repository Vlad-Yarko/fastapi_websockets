from starlette.endpoints import WebSocketEndpoint

from src.utils.ws_manager import WSManager


class WSNotification(WSManager, WebSocketEndpoint):
    pass
