"""Message Class Context"""

# Libraries
from json import dumps
from datetime import datetime


class Message:
    message: str = ""
    channel: str = ""

    def __init__(self, id: str, origin: str):
        self.id = id
        self.origin = origin

    def now(self):
        self.timestamp = datetime.now()

    def __str__(self):
        self.now()
        return str(dumps({
            "id": self.id,
            "origin": self.origin,
            "timestamp": self.timestamp.isoformat(),
            "message": self.message,
            "channel": self.channel,
        }))
