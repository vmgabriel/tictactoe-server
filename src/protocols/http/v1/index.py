"""Routes of http"""

# Libraries
from datetime import datetime
from flask import Blueprint, jsonify, url_for


from src.extensions import get_server

router = Blueprint("", __name__)

@router.route("v1/")
def base():
    """Route Base Configuration"""
    return jsonify({
        "api": "active"
    }), 200

@router.route("v1/games")
def list_games(*args, **kwargs):
    """All List of Games"""
    server = get_server()
    channels = server.channels
    datas = [channel.to_json() for channel in channels if channel.route != ""]
    return jsonify({
        "count": len(datas),
        "datas": datas,
    }), 200
