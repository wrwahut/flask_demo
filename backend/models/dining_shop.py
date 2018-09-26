# -*- coding:utf-8 -*-

from .base import CRUD
from . import db

class Dining_shop(CRUD,db.Model):
    __bind_key__ = "other"

    id = db.Column(db.Integer, primary_key=True)
    shop_name = db.Column(db.VARCHAR(60))
    true_name = db.Column(db.VARCHAR(255))
    address = db.Column(db.VARCHAR(255))
    img_url = db.Column(db.VARCHAR(255))
    thumb = db.Column(db.Integer)
    phone = db.Column(db.Integer)
    user_id = db.Column(db.VARCHAR(255))
    account = db.Column(db.VARCHAR(255))
    updown = db.Column(db.Integer)
    start_time = db.Column(db.VARCHAR(255))
    end_time = db.Column(db.VARCHAR(255))
    content = db.Column(db.VARCHAR(255))
    add_time = db.Column(db.VARCHAR(255))
    deal_money = db.Column(db.FLOAT)
    sort = db.Column(db.Integer)
    send_price = db.Column(db.VARCHAR(255))
    total_count = db.Column(db.Integer)
    left_money = db.Column(db.FLOAT)
    recommend = db.Column(db.Integer)
    tel_phone = db.Column(db.VARCHAR(11))
    success_fee = db.Column(db.FLOAT)
    plate_fee = db.Column(db.FLOAT)
    full_cut = db.Column(db.Text)
    is_full_cut = db.Column(db.Integer)
    discount = db.Column(db.VARCHAR(255))
    is_discount = db.Column(db.Integer)
    score = db.Column(db.Integer)
    star = db.Column(db.Integer, default=7)
    complain_count = db.Column(db.Integer,default=0)
    box_fee = db.Column(db.FLOAT)