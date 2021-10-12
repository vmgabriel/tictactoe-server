"""App content"""

from flask import Flask

# Config
from .config import config

# Register Protocols
from .protocols import register_http, register_ws
from .extensions import register_ws_extensions


def create_app():
    """Create the APP"""
    app = Flask(__name__)
    app.config.from_object(config)

    register_http(app)
    socket, emitter = register_ws_extensions(app)
    register_ws(socket, emitter)
    # register_extensions(app)

    return app


def create_worker_app():
    pass


def create_event_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # socket, emitter = register_ws_extensions(app)
    # register_ws(socket, emitter)

    return app
