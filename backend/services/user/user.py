# coding:utf-8
from backend.models import *
from flask import g, request, jsonify, render_template
from backend.common import query_from_argument, query_from_json, error_handler, Redisi
from . import bp_user

import time
import datetime
import json

time_format = "%Y-%m-%d"

@bp_user.route("/user_init", methods=["POST", "GET"])
@error_handler
def user_init():
    args = request.json
    db.create_all()
    return jsonify({"re": "200", "msg": "success", "data": {}})

@bp_user.route("/update_push_cid", methods=["POST", "GET"])
@error_handler
def update_push_cid():
    args = request.json
    if args.get("phone","") and args.get("cid",""):
        return jsonify({"re": "402", "msg": "param_error", "data": {}})
    query = {"phone": args["phone"]}
    shop = query_from_argument(Dining_shop, query).first()
    if shop:
        query["user_id"] = shop.user_id
        # query["cid"] = args["cid"]
        user = query_from_argument(Base_user, {"id": shop.user_id}).first()
        if user:
            query["shop_id"] = user.shop_id
        push_info = query_from_argument(User, query).first()
        if push_info:
            push_info.change_data({"cid": args["cid"]})
        else:
            push_info = User()
            query["cid"] = args["cid"]
            push_info.init(query)
        return jsonify({"re": "200", "msg": "success", "data": {}})
    return jsonify({"re": "404", "msg": "no_shop", "data": {}})
        

@bp_user.route("/sign_in", methods=["POST"])
@error_handler
def sign_in():
    args = request.json
    # args = {}
    # args["phone"] = "18956537890"
    if args.get("phone"):
        shop = query_from_argument(Dining_shop, {"phone": args["phone"]}).first()
        if shop:
            token_data = {"user_id": shop.user_id, "phone": args["phone"]}
            user = query_from_argument(Base_user, {"id": shop.user_id}).first()
            if user:
                token_data["shop_id"] = user.shop_id
            if args.get("cid"):
                user_cid = query_from_argument(User, {"shop_id": user.shop_id}).first()
                if user_cid:
                    user_cid.change_data({"cid": args["cid"]})
                else:
                    user_cid = User()
                    query_init = {"cid": args["cid"], "shop_id": user.shop_id, "user_id": shop.user_id}
                    user_cid.init(query_init)
            return jsonify({"re": "200", "msg": "success", "data": {}})
            # return jsonify({"re": "200", "msg": "success", "data": {"data": {}, "token": token_data}})
        return jsonify({"re": "404", "msg": "phone_none", "data": {}})
    return jsonify({"re": "402", "msg": "param_error", "data": {}})

@bp_user.route("/get_user_order", methods=["POST"])
@error_handler
def get_user_order():
    data = []
    total_num = 0
    now = datetime.datetime.fromtimestamp(time.time()).strftime(time_format)
    local_orders = query_from_argument(Order, {"shop_id": g.shop_id, "status": 0}).filter(Order.pay_time == now)
    total_num = local_orders.count()
    local_orders = local_orders.order_by(Order.id.desc()).offset(int(args["startNum"])).limit(args["pageSize"])
    local_orders = local_orders.all()
    for local_order in local_orders:
        order = query_from_argument(Dining_order, {"shop_id": g.shop_id, "order_num": local_order.order_num}).first()
        if order:
            info = {}
            info["index"] = local_order.index
            info["order_num"] = order.order_num
            info["shop_name"] = order.shop_name
            info["add_time"] = order.add_time
            info["pay_time"] = order.pay_time
            info["sender_phone"] = (order.sender_phone if order.sender_phone else "-")
            info["sender_name"] =  "-"
            info["sender_sex"] = "-"
            info["shop_address"] = "-"
            address_json = eval(order.address_json)
            sender = query_from_argument(Dining_sender, {"id": order.sender_id}).first()
            if sender:
                info["sender_name"] = sender.true_name
                info["sender_sex"] = ("male" if sender.sex ==1 else "female")
            shop = query_from_argument(Dining_shop, {"id": g.shop_id}).first()
            if shop:
                info["shop_address"] = shop.address
            info["user_name"] = address_json.get("call_name")
            info["user_phone"] = address_json.get("phone")
            info["user_address"] = address_json.get("address")
            info["message"] = order.message
            info["fee"] = order.fee
            info["person_count"] = order.person_count
            info["shop_phone"] = order.shop_phone
            info["total_box_fee"] = order.total_box_fee
            info["status"] = order.status
            goods = json.loads(order.goods_list)
            total_price = 0
            for good in goods:
                total_price += float(good.get("total_price","0"))
            info["price"] = total_price + float(order.fee)
            info["goods"] = goods
            data.append(info)
    return jsonify({"re": "200", "msg": "success", "data": {"detail":data, "total_num": total_num}})

@bp_user.route("/get_all_orders", methods=["POST"])
@error_handler
def get_all_orders():
    args = request.json
    data = []
    total_num = 0
    now = datetime.datetime.fromtimestamp(time.time()).strftime(time_format)
    local_orders = query_from_argument(Order, {"shop_id": g.shop_id}).filter(Order.pay_time == now)
    total_num = local_orders.count()
    local_orders = local_orders.order_by(Order.id.desc()).offset(int(args["startNum"])).limit(args["pageSize"])
    local_orders = local_orders.all()
    for local_order in local_orders:
        order = query_from_argument(Dining_order, {"shop_id": g.shop_id, "order_num": local_order.order_num}).first()
        if order:
            info = {}
            info["index"] = local_order.index
            info["order_num"] = order.order_num
            info["shop_name"] = order.shop_name
            info["add_time"] = order.add_time
            info["pay_time"] = order.pay_time
            info["sender_phone"] = (order.sender_phone if order.sender_phone else "-")
            info["sender_name"] =  "-"
            info["sender_sex"] = "-"
            info["shop_address"] = "-"
            address_json = eval(order.address_json)
            sender = query_from_argument(Dining_sender, {"id": order.sender_id}).first()
            if sender:
                info["sender_name"] = sender.true_name
                info["sender_sex"] = ("male" if sender.sex ==1 else "female")
            shop = query_from_argument(Dining_shop, {"id": g.shop_id}).first()
            if shop:
                info["shop_address"] = shop.address
            info["user_name"] = address_json.get("call_name")
            info["user_phone"] = address_json.get("phone")
            info["user_address"] = address_json.get("address")
            info["message"] = order.message
            info["fee"] = order.fee
            info["person_count"] = order.person_count
            info["shop_phone"] = order.shop_phone
            info["total_box_fee"] = order.total_box_fee
            info["status"] = order.status
            goods = json.loads(order.goods_list)
            total_price = 0
            for good in goods:
                total_price += float(good.get("total_price","0"))
            info["price"] = total_price + float(order.fee)
            info["goods"] = goods
            data.append(info)
    return jsonify({"re": "200", "msg": "success", "data": {"detail":data, "total_num": total_num}})

@bp_user.route("/print_order", methods=["POST"])
@error_handler
def print_order():
    args = request.json
    order_num = args["order_num"]
    order = query_from_argument(Order, {"shop_id": g.shop_id, "order_num": order_num}).first()
    if order:
        order.change_data({"status": 1})
    return jsonify({"re": "200", "msg": "success", "data": {}})



@bp_user.route("/get_printed_orders", methods=["POST"])
@error_handler
def get_printed_orders():
    args = request.json
    data = []
    total_num = 0
    now = datetime.datetime.fromtimestamp(time.time()).strftime(time_format)
    local_orders = query_from_argument(Order, {"shop_id": g.shop_id, "status": 1}).filter(Order.pay_time == now)
    total_num = local_orders.count()
    local_orders = local_orders.order_by(Order.id.desc()).offset(int(args["startNum"])).limit(args["pageSize"])
    local_orders = local_orders.all()
    for local_order in local_orders:
        order = query_from_argument(Dining_order, {"shop_id": g.shop_id, "order_num": local_order.order_num}).first()
        if order:
            info = {}
            info["index"] = local_order.index
            info["order_num"] = order.order_num
            info["shop_name"] = order.shop_name
            info["add_time"] = order.add_time
            info["pay_time"] = order.pay_time
            info["sender_phone"] = (order.sender_phone if order.sender_phone else "-")
            info["sender_name"] =  "-"
            info["sender_sex"] = "-"
            info["shop_address"] = "-"
            address_json = eval(order.address_json)
            sender = query_from_argument(Dining_sender, {"id": order.sender_id}).first()
            if sender:
                info["sender_name"] = sender.true_name
                info["sender_sex"] = ("male" if sender.sex ==1 else "female")
            shop = query_from_argument(Dining_shop, {"id": g.shop_id}).first()
            if shop:
                info["shop_address"] = shop.address
            info["user_name"] = address_json.get("call_name")
            info["user_phone"] = address_json.get("phone")
            info["user_address"] = address_json.get("address")
            info["message"] = order.message
            info["fee"] = order.fee
            info["person_count"] = order.person_count
            info["shop_phone"] = order.shop_phone
            info["total_box_fee"] = order.total_box_fee
            info["status"] = order.status
            goods = json.loads(order.goods_list)
            total_price = 0
            for good in goods:
                total_price += float(good.get("total_price","0"))
            info["price"] = total_price + float(order.fee)
            info["goods"] = goods
            data.append(info)
    return jsonify({"re": "200", "msg": "success", "data": {"detail":data, "total_num": total_num}})

def handler_time(dt):
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    today_ctime = int(time.mktime(timeArray))
    return today_ctime
