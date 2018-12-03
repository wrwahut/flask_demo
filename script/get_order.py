# coding: utf-8 
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import traceback
import time
import datetime
import json

from models import *
import script_config
from conntect import Caller
from push_message import  pushMessageToSingle

time_format = "%Y-%m-%d"

@script_config.sessionhandler
def main(session=None):
    now = datetime.datetime.fromtimestamp(time.time()).strftime(time_format)
    orders = session.query(Dining_order).filter(Dining_order.status.in_(tuple([3])))
    orders = orders.filter(Dining_order.pay_time.like("%" + now + "%"))
    orders = orders.order_by(Dining_order.id.asc())
    orders = orders.all()
    if orders:
        for order in orders:
            flag, index = get_order_local(order.shop_id, order.order_num)
            if flag:
                continue
            print "###################",order.id, "%%%%%%%%%%%%",order.order_num
            cid = get_user_cid(order.shop_id)
            info = {}
            info["index"] = index
            info["order_num"] = order.order_num
            info["shop_name"] = order.shop_name
            info["add_time"] = order.add_time
            info["pay_time"] = order.pay_time
            info["sender_phone"] = (order.sender_phone if order.sender_phone else "-")
            info["sender_name"] =  "-"
            info["sender_sex"] = "-"
            info["shop_address"] = "-"
            address_json = eval(order.address_json)
            sender = session.query(Dining_sender).filter(Dining_sender.id ==  order.sender_id).first()
            if sender:
                info["sender_name"] = sender.true_name
                info["sender_sex"] = ("male" if sender.sex ==1 else "female")
            shop = session.query(Dining_shop).filter(Dining_shop.id == order.shop_id).first()
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
            # cid = "8713dd61d415c9806bd3d3f3716a0293"
            if cid:
                print "@@@@@@@@@@@@@@@@@@@@@@@@info=",json.dumps(info,"utf-8")
                pushMessageToSingle(cid, json.dumps(info,"utf-8"))
            # Caller("send_jpush", {"shop_id": order.shop_id, "order_num": order.order_num}).post_req()

@script_config.sessionhandler2
def get_order_local(shop_id, order_num, session=None):
    local_orders = session.query(Order).filter(Order.order_num == order_num).first()
    if local_orders:
        return True, local_orders.index
    else:
        now = datetime.datetime.fromtimestamp(time.time()).strftime(time_format)
        count_order = session.query(Order).filter(Order.shop_id == shop_id, Order.pay_time == now).count()
        order = Order()
        init_query = {"shop_id":shop_id, "order_num": order_num, "pay_time": now, "index": count_order+ 1}
        order.init(init_query, session)
        return False, count_order+ 1

@script_config.sessionhandler2
def get_user_cid(shop_id, session):
    cid = ""
    shop = session.query(User).filter(User.shop_id == shop_id).first()
    if shop:
        cid = shop.cid
    return cid


        


if __name__ == "__main__":
    # Caller("send_jpush", {"shop_id": 173, "order_num": "23432422"}).post_req()
    env = "online"
    script_config.init(env)
    try:
        while True:
            main()
            time.sleep(10)
    except Exception,e:
        traceback.print_exc()
        time.sleep(10)
