# coding:utf-8
from backend.models import *
from flask import g, request, jsonify, render_template
from backend.common import query_from_argument, query_from_json, error_handler, Redisi
from . import bp_user

from time import time
from datetime import datetime

time_format = "%Y-%m-%d"

@bp_user.route("/user_init", methods=["POST", "GET"])
@error_handler
def user_init():
    args = request.json
    print "%%%%%%%%%%%%%", g.phone, g.user_id, g.shop_id
    return jsonify({"re": "200", "msg": "success", "data": {}})

@bp_user.route("/sign_in", methods=["POST", "GET"])
@error_handler
def sign_in():
    args = request.json
    args = {}
    # args["phone"] = "18956537890"
    if args.get("phone"):
        shop = query_from_argument(Dining_shop, {"phone": args["phone"]}).first()
        if shop:
            token_data = {"user_id": shop.user_id, "phone": args["phone"]}
            user = query_from_argument(Base_user, {"id": shop.user_id}).first()
            if user:
                token_data["shop_id"] = user.shop_id
            return jsonify({"re": "200", "msg": "success", "data": {"data": {}, "token": token_data}})
        return jsonify({"re": "404", "msg": "phone_none", "data": {}})
    return jsonify({"re": "402", "msg": "param_error", "data": {}})

@bp_user.route("/get_user_order", methods=["POST", "GET"])
@error_handler
def get_user_order():
    data = []
    now = datetime.fromtimestamp(time()).strftime(time_format)
    orders = query_from_argument(Dining_order, {"shop_id": g.shop_id})
    print "###########$$$$$$$$$$$$$$$",orders.count()
    orders = orders.filter(Dining_order.status.in_(tuple([3,4])))
    print "###########$$$$$$$$$$$$$$$",orders.count()
    orders = orders.filter(Dining_order.pay_time.like("%" + "2018-09-25" + "%"))
    orders = orders.order_by(Dining_order.id.desc())
    orders = orders.all()
    if orders:
        for order in orders:
            info = {}
            info["order_num"] = order.order_num
            info["shop_name"] = order.shop_name
            info["add_time"] = order.add_time
            info["pay_time"] = order.pay_time
            info["sender_phone"] = order.sender_phone
            address_json = eval(order.address_json)
            sender = query_from_argument(Dining_sender, {"id": order.sender_id}).first()
            if sender:
                info["sender_name"] = sender.true_name
                info["sender_sex"] = ("male" if sender.sex ==1 else "female")
            info["user_name"] = address_json.get("call_name")
            info["user_phone"] = address_json.get("phone")
            info["user_address"] = address_json.get("address")
            info["message"] = order.message
            info["fee"] = order.fee
            info["person_count"] = order.person_count
            info["shop_phone"] = order.shop_phone
            info["total_box_fee"] = order.total_box_fee
            goods = eval(order.goods_list)
            info["goods"] = goods
            order_local = query_from_argument(Order, {"order_num": order.order_num}).first()
            if order_local:
                if order_local.status == 1:
                    continue
            else:
                order_local = Order()
                order_local.init({"status": 0, "order_num": order.order_num, "shop_id":g.shop_id})

            # print "@@@@@@@@@@@@@", order.user_id, "^^^^^^^",g.shop_id
            # print "###############", goods
            data.append(info)
            # break
    return jsonify({"re": "200", "msg": "success", "data": data})

@bp_user.route("/get_all_orders", methods=["POST","GET"])
@error_handler
def get_all_orders():
    data = []
    orders = query_from_argument(Dining_order, {"shop_id": g.shop_id, "status": 5})
    # orders = orders.outerjoin(Order, Order.order_num == Dining_order.order_num)
    orders = orders.order_by(Dining_order.id.desc())
    orders = orders.all()
    if orders:
        for order in orders:
            info = {}
            info["order_num"] = order.order_num
            info["shop_name"] = order.shop_name
            info["add_time"] = order.add_time
            info["pay_time"] = order.pay_time
            info["sender_phone"] = order.sender_phone
            address_json = eval(order.address_json)
            sender = query_from_argument(Dining_sender, {"id": order.sender_id}).first()
            if sender:
                info["sender_name"] = sender.true_name
                info["sender_sex"] = ("male" if sender.sex ==1 else "female")
            info["user_name"] = address_json.get("call_name")
            info["user_phone"] = address_json.get("phone")
            info["user_address"] = address_json.get("address")
            info["message"] = order.message
            info["fee"] = order.fee
            info["person_count"] = order.person_count
            info["shop_phone"] = order.shop_phone
            info["total_box_fee"] = order.total_box_fee
            goods = eval(order.goods_list)
            info["goods"] = goods
            data.append(info)
    return jsonify({"re": "200", "msg": "success", "data": data})

@bp_user.route("/print_order", methods=["POST", "GET"])
@error_handler
def print_order():
    args = request.json
    order_num = args["order_num"]
    order = query_from_argument(Order, {"shop_id": g.shop_id, "order_num": order_num}).first()
    if order:
        order.change_data({"status": 1})
    return jsonify({"re": "200", "msg": "success", "data": {}})