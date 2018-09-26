# coding:utf-8
from functools import wraps
import traceback
from backend.models import db
from flask import jsonify

def error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            data = func(*args, **kwargs)
            db.session.commit()
            return data
        except Exception, e:
            db.session.rollback()
            traceback.print_exc()
            return jsonify({"re": "500", "msg": u"程序错误", "data": str(e)})
    return wrapper