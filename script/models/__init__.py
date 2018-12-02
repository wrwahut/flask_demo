# -*- coding:utf-8 -*-

# from backend.extensions import db
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# from user import User
# from base_user import Base_user
from dining_shop import Dining_shop
from dining_order import Dining_order
from dining_sender import Dining_sender
from dining_goods import Dining_goods
from order import Order
from user import User