"""Server WS Event"""

# Libraries
from typing import List
from enum import Enum

# Modules
from .channel import Channel
from .message import Message
from .adapter import WSAdapter


class MessageType(str, Enum):
    UNICAST = "unicast"
    MULTICAST = "multicast"
    BROADCAST = "broadcast"


class Server:
    def __init__(self, emitter: WSAdapter):
        self.channels: List[Channel] = []
        self.emitter = emitter

    def get_channel(self, route: str) -> Channel:
        for channel in self.channels:
            if channel.route == route:
                return channel
        return None

    def remove_channel(self, route: str):
        channels = []
        for channel in self.channels:
            if channel.route != route:
                channels.append(channel)
        self.channels = channels


    def channel(self, path: str, consumer: object, id: str):
        """Create or Update consumer in channel"""
        channel_path = self.get_channel(path)
        if not channel_path:
            channel_path = Channel(path)
            self.channels.append(channel_path)
        channel_path.add_consumer(consumer, id)

    def remove_consumer_channel(self, path: str, consumer: object):
        channel = self.get_channel(path)
        if channel:
            channel.remove_consumer(str(consumer.id))

    def broadcast(self, message: str):
        message = Message("SERVER", "SERVER")
        message.message = message
        for channel in self.channels:
            channel.broadcast("SERVER", message)


    def output(self, message: dict, channel: str, message_type: MessageType, origin: str, dst: List[str] = None):
        """Send Message to Destinatary(ies)
        message: The Message to Send
        channel: The Channel to find destinataries
        dst: Destinatary(ies) -> List of users to send message if the destinatary is not in channel this ignore
        message_type: the message type is the mode of message
        """
        if message_type == message_type.UNICAST:
            if 0 <= len(dst) > 1:
                raise Exception("[Error] - Unique User not valid")
            self.get_channel(channel).unicast(origin, dst, message)

        if message_type == message_type.BROADCAST:
            self.get_channel(channel).broadcast(origin, message)

        if message_type == message_type.MULTICAST:
            if len(dst) < 2:
                raise Exception("[Error] - Only One User in message Multicast")
            self.get_channel(channel).multicast(origin, dst, message)
