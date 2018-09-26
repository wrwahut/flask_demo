# -*- coding:utf-8 -*-

from .base import CRUD
from . import db

class Dining_sender(CRUD,db.Model):
    __bind_key__ = "other"

    id = db.Column(db.Integer, primary_key=True)
    true_name = db.Column(db.VARCHAR(255))
    user_id = db.Column(db.Integer)
    account = db.Column(db.VARCHAR(255))
    phone = db.Column(db.VARCHAR(255))
    is_use = db.Column(db.Integer, default=1)
    time_ids = db.Column(db.VARCHAR(255))
    skimp_money = db.Column(db.FLOAT)
    sex = db.Column(db.Text)
    add_time = db.Column(db.Integer)
    last_time = db.Column(db.VARCHAR(255))
    total_times = db.Column(db.Integer)
    shop_ids = db.Column(db.VARCHAR(255))
    build_ids = db.Column(db.VARCHAR(255))
    zan_count = db.Column(db.Integer, default=0)