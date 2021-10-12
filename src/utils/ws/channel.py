"""Load Channels configuration"""

# Libraries
from typing import List

from .message import Message


class Channel:
    """Channel for each route"""
    def __init__(self, route: str):
        self.route: str = route
        self.consumers = {}
        self.instance: object = None

    def add_consumer(self, consumer: object, id: str):
        """Add a new consumer
        the consumer is dict as object.consumer
        """
        if id not in self.consumers:
            self.consumers[id] = consumer

    def get_consumer(self, id: str) -> object:
        """Get consumer with id"""
        return self.consumers.get(id, None)

    def remove_consumer(self, id: str) -> object:
        """Remove Consumer Based in id"""
        consumer = self.consumers.get(id, None)
        if consumer:
            del self.consumers[id]
        return consumer

    def consumer_connected(self):
        consumers = {}
        for id, consumer in self.consumers.items():
            if consumer.connected:
                consumers[id] = consumer
        return consumers

    def unicast(self, origin: str, id_consumer: List[str], message: Message):
        """Send Message to unique user with id_consumer"""
        consumer = self.get_consumer(id_consumer[0])
        try:
            consumer.send(str(message))
        except Exception as exc:
            self.remove_consumer(id_consumer[0])

    def multicast(self, origin: str, id_consumers: List[str], message: Message):
        """Send Message to specific users"""
        self.consumers = self.consumer_connected()
        for id_consumer in self.consumers:
            self.unicast(origin, id_consumer, message)

    def broadcast(self, origin: str, message: Message) -> int:
        """Send Message to All consumers of Channel"""
        self.consumers = self.consumer_connected()
        counter = 0
        for id, consumer in self.consumers.items():
            counter += 1
            self.unicast(origin, [id], message)
        return counter

    def __str__(self):
        return f"Channel {self.route} - consumers: {self.consumers}"

    def __repr__(self):
        return str(self)
