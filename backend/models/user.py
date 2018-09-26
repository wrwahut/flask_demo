# -*- coding:utf-8 -*-

from .base import CRUD
from . import db

class User(CRUD,db.Model):
    __tablename__ = "user"
    # __bind_key__ = "other"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.CHAR(200), unique=True)
    username = db.Column(db.CHAR(200), unique=True)
    age = db.Column(db.Integer)
    email = db.Column(db.CHAR(200))
    data = db.Column(db.JSON)
    sex = db.Column(db.CHAR(20))