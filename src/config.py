"""Configuration of Project"""

import os
from dotenv import load_dotenv
from pathlib import Path


env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


HOST_WS = os.getenv("HOST")
PORT_WS = os.getenv("PORT")
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "on", "1", "t")
SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(16).hex())


class Config:
    """Configuration"""
    DEBUG = DEBUG
    SECRET_KEY = SECRET_KEY


config = Config
