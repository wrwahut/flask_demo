# -*- coding:utf-8 -*-

from .base import CRUD
from . import db

class Dining_goods(CRUD,db.Model):
    __bind_key__ = "other"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(255))
    shop_id = db.Column(db.Integer)
    img_url = db.Column(db.VARCHAR(255))
    thumb = db.Column(db.VARCHAR(255))
    updown = db.Column(db.Integer, default=1)
    simple_desc = db.Column(db.VARCHAR(255))
    sale_quantity = db.Column(db.FLOAT)
    price = db.Column(db.FLOAT)
    sort_num = db.Column(db.Integer)
    ori_price = db.Column(db.FLOAT)
    inventory = db.Column(db.Integer)
    uint = db.Column(db.VARCHAR(255))
    updown_time = db.Column(db.VARCHAR(255))
    recommend = db.Column(db.Integer, default=0)
    add_time = db.Column(db.VARCHAR(255))
    self_fee_ratio = db.Column(db.FLOAT)
    parent_fee_ratio = db.Column(db.FLOAT)
    grand_fee_ratio = db.Column(db.FLOAT)
    comment_count = db.Column(db.Integer)
    comment_score = db.Column(db.FLOAT)
    points = db.Column(db.Integer)
    detail_desc = db.Column(db.Text)
    shop_name = db.Column(db.VARCHAR(255))
    is_box_fee = db.Column(db.Integer)