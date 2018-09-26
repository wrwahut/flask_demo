# -*- coding:utf-8 -*-

from .base import CRUD
from . import db

class Base_user(CRUD,db.Model):
    # __tablename__ = "user"
    __bind_key__ = "other"

    id = db.Column(db.Integer, primary_key=True)
    nick_name = db.Column(db.VARCHAR(60))
    open_id = db.Column(db.VARCHAR(255))
    account = db.Column(db.VARCHAR(255))
    password = db.Column(db.VARCHAR(255))
    sex = db.Column(db.Integer)
    subscribe = db.Column(db.Integer)
    country = db.Column(db.VARCHAR(255))
    province = db.Column(db.VARCHAR(255))
    city = db.Column(db.VARCHAR(255))
    detail = db.Column(db.VARCHAR(255))
    head_img_url = db.Column(db.VARCHAR(255))
    subscribe_time = db.Column(db.VARCHAR(255))
    remark = db.Column(db.VARCHAR(255))
    group_id = db.Column(db.VARCHAR(255))
    email = db.Column(db.VARCHAR(60))
    phone = db.Column(db.VARCHAR(255))
    birthday = db.Column(db.VARCHAR(255))
    subscribe_times = db.Column(db.Integer)
    subscribe_type = db.Column(db.Integer)
    points = db.Column(db.Integer)
    total_fee = db.Column(db.FLOAT)
    balance = db.Column(db.FLOAT)
    shop_id = db.Column(db.Integer)
    sender_id = db.Column(db.Integer)
    name = db.Column(db.VARCHAR(255))
    con_sign_days = db.Column(db.Integer)
    donate_money = db.Column(db.FLOAT)
    donate_quantity = db.Column(db.Integer)
    duo_coin = db.Column(db.Integer)

    is_agent = db.Column(db.VARCHAR(255))
    cash_points_money = db.Column(db.Integer)
    cash_points_money = db.Column(db.Integer)
    cash_points = db.Column(db.Integer)
    signature = db.Column(db.VARCHAR(255))
    user_id = db.Column(db.VARCHAR(255))
    parent_id = db.Column(db.VARCHAR(10))
    is_first_order = db.Column(db.VARCHAR(1))