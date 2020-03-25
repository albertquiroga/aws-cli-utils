from common_utils import DEFAULT_SSH_OPTIONS


class ConnectionParams:
    def __init__(self, host: str, username: str, port: int = 22, key: str = "", options: str = DEFAULT_SSH_OPTIONS):
        self.host = host
        self.port = port
        self.username = username
        self.key = key
        self.options = options
