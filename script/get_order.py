# coding: utf-8 
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import traceback
import time

from models import *
import script_config


@script_config.sessionhandler
def main(session=None):
    orders = session.query(Dining_order).filter(Dining_order.shop_id == "173").first()
    if orders:
        print "###################", orders.goods_list
        


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