"""Routes of http"""

# Libraries
from datetime import datetime
from flask import Blueprint, jsonify, url_for


router = Blueprint("", __name__)

@router.route("v1/")
def base():
    """Route Base Configuration"""
    return jsonify({
        "hello": "world"
    }), 200
