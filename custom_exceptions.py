class DisallowedConnection(Exception):
    def __init__(self, status):
        self.status = status
