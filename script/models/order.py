# -*- coding:utf-8 -*-

from .base import CRUD
from . import db

class Order(CRUD,db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer,default = 0)  # 0     1     2
    ctime = db.Column(db.Integer)
    shop_id = db.Column(db.VARCHAR(255))
    data = db.Column(db.JSON)