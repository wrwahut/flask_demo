# coding: utf-8 
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import traceback
import time
import datetime

from models import *
import script_config
from conntect import Caller

time_format = "%Y-%m-%d"

@script_config.sessionhandler
def main(session=None):
    now = datetime.datetime.fromtimestamp(time.time()).strftime(time_format)
    orders = session.query(Dining_order).filter(Dining_order.status.in_(tuple([3,4])))
    orders = orders.filter(Dining_order.pay_time.like("%" + now + "%"))
    orders = orders.order_by(Dining_order.id.asc())
    orders = orders.all()
    if orders:
        for order in orders:
            flag = get_order_local(order.shop_id, order.order_num)
            if flag:
                continue
            print "###################", order.id, "%%%%%%%%%%%%",order.order_num
            # Caller("send_jpush", {"shop_id": order.shop_id, "order_num": order.order_num}).post_req()

@script_config.sessionhandler2
def get_order_local(shop_id, order_num, session=None):
    local_orders = session.query(Order).filter(Order.order_num == order_num).first()
    if local_orders:
        return True
    else:
        now = datetime.datetime.fromtimestamp(time.time()).strftime(time_format)
        count_order = session.query(Order).filter(Order.shop_id == shop_id, Order.pay_time == now).count()
        order = Order()
        init_query = {"shop_id":shop_id, "order_num": order_num, "pay_time": now, "index": count_order+ 1}
        order.init(init_query, session)
        return False

        


if __name__ == "__main__":
    env = "online"
    script_config.init(env)
    try:
        while True:
            main()
            time.sleep(10)
    except Exception,e:
        traceback.print_exc()
        time.sleep(10)