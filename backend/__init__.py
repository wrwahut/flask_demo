# -*- coding:utf-8 -*-

from backend.app import create_app, app
import time
from uuid import uuid1
from flask import g, request, jsonify, make_response, json
from extensions import db, socketio
# from backend.common import Redisi
from backend.common import query_from_argument, query_from_json, error_handler, Redisi
from backend.models import *

no_token = ["sign_in"]

@app.before_request
def before_request():
    g.path = request.path
    funcName =  g.path.split("/")[-1]
    print "###########################funcName=", funcName
    if not funcName in ["user_init"]:
        phone = request.json.get("phone","")
        data = get_user_Info(phone)
        print "@@@@@@@@@@@@@@@@@@@@@@",data
        g.phone = data.get("phone", "")
        g.user_id = data.get("user_id", "")
        g.shop_id = data.get("shop_id", "")
    # if not funcName in no_token:
    #     cookie = dict(request.cookies)
    #     token = cookie.get("token", "")
    #     if token:
    #         data = Redisi().get_data(token)
    #         if not data:
    #             return jsonify({"re": "405", "msg": "token expired", "data": {}})
    #         data = eval(data)
    #         g.phone = data.get("phone", "")
    #         g.user_id = data.get("user_id", "")
    #         g.shop_id = data.get("shop_id", "")
    #     print "@@@@@@@@@@@@@cookie=", cookie


@app.after_request
def after_request(response):
    print "after_request:\n request path ---------", g.path
    funcName = g.path.split("/")[-1]
    # if response.status_code == 200:
    #     redata = json.loads(response.data)
    #     if funcName in ["sign_in"] and redata["re"] == "200":
    #         token = generate_token()
    #         res = make_response(jsonify(redata["data"]["data"]))
    #         res.set_cookie("token", token)
    #         Redisi().set_data(token, str(redata["data"]["token"]), 200*60)
    #         return res
    return response

def get_user_Info(phone):
    shop = query_from_argument(Dining_shop, {"phone": phone}).first()
    if shop:
        token_data = {"user_id": shop.user_id, "phone": phone}
        user = query_from_argument(Base_user, {"id": shop.user_id}).first()
        if user:
            token_data["shop_id"] = user.shop_id
            return token_data
    return {}
    
def generate_token():
    token = "a" + str(uuid1()).replace("-", "")
    return token