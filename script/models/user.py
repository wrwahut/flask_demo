# -*- coding:utf-8 -*-

from .base import CRUD
from . import db

class User(CRUD,db.Model):
    __tablename__ = "user"
    # __bind_key__ = "other"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.CHAR(200), unique=True)
    phone = db.Column(db.CHAR(200), unique=True)
    shop_id = db.Column(db.CHAR(200),unique=True)
    user_id = db.Column(db.CHAR(200),unique=True)
    cid = db.Column(db.CHAR(200))
    data = db.Column(db.JSON)