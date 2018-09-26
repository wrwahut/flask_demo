# -*- coding:utf-8 -*-

from flask import Flask
from .extensions import db, redis, socketio
from backend.services import *

app = Flask(__name__)

def create_app(config=None):
    app.config.from_object(config)
    configure_extension(app)
    configure_blueprint(app)
    return app

def configure_extension(app):
    db.init_app(app)
    redis.init_app(app)
    socketio.init_app(app)

def configure_blueprint(app):
    app.register_blueprint(bp_user, url_prefix="/resource/user")