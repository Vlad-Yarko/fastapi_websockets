from collections import defaultdict


class ConnectionManager:
    def __init__(self):
        self.active_connections = defaultdict(set)
        self.active_tasks = defaultdict(str)
        self.websocket_to_user_id = defaultdict(str)


connection_manager = ConnectionManager()
