"""Protocols"""

# Libraries
from flask import Flask
from flask_sock import Sock

# All Http
from .http import all_http
from .ws import socket


def register_http(app: Flask):
    for version in all_http:
        for url in version:
            app.register_blueprint(url, url_prefix="/api")


def register_ws(sock: Sock, emitter):
    socket(sock, emitter)
