# -*- coding:utf-8 -*-

from .base import CRUD
from . import db

class Order(CRUD,db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer,default = 0)  # 0     1     2
    shop_id = db.Column(db.VARCHAR(255))
    order_num = db.Column(db.VARCHAR(255))