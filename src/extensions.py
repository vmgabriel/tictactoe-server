"""Extensions of Project"""

# Libraries
from typing import Tuple
from flask import Flask
from flask_sock import Sock

from src.utils.ws.server import Server
from src.utils.ws.adapter import WSAdapter

# Modules
from src.tictactoe.events import events


def register_ws_extensions(app: Flask) -> Tuple[Sock, Server]:
    """Register WS Extensions"""
    server = get_server()
    return Sock(app), server


def get_server():
    emitter = WSAdapter()
    for event in events:
        emitter.add_event(event())
    server = Server.instance(emitter)
    return server
