# -*- coding:utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from flask_socketio import SocketIO

db = SQLAlchemy()
redis = FlaskRedis()
socketio = SocketIO()