from bertolb_utils import DEFAULT_SSH_OPTIONS


class ConnectionParams:
    def __init__(self, host, username, port=22, key="", options=DEFAULT_SSH_OPTIONS):
        self.host = host
        self.port = port
        self.username = username
        self.key = key
        self.options = options
