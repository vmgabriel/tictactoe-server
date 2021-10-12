"""WS Adapter"""

# Libraries
from datetime import datetime
from typing import List, Dict
from abc import ABC, abstractmethod

# Modules
from .channel import Channel


class EventWS(ABC):
    @abstractmethod
    def __init__(self):
        self._event_title = ""

    @property
    def event_title(self) -> str:
        return self._event_title

    @abstractmethod
    def event(self, origin: str, channel: Channel,  message: dict, server: object):
        pass


class WSAdapter:
    def __init__(self):
        self.events: Dict[str, EventWS] = {}

    def get_event(self, name: str):
        return self.events.get(name, None)

    def add_event(self, event: EventWS):
        name_event = event.event_title
        if name_event not in self.events:
            self.events[name_event] = event

    def emit(self, origin: str, channel: Channel, message: dict, server: object):
        """Emit Event Context"""
        activator = message["event_name"]
        eventer = self.get_event(activator)
        if not eventer:
            raise Exception("[Error] Event not exist")
        eventer.event(origin, channel, message, server)
