# coding:utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import traceback
import redis
from sqlalchemy.ext.declarative import declarative_base


db_online = {
    "db_connect_string": "mysql+mysqldb://root:qwer1234@localhost/wrwahut?charset=utf8",
    "db_dining": "mysql+mysqldb://root:cjb.123456!@47.104.89.74/cjbsp?charset=utf8",
    "Tredis": {
        "host": "localhost",
        "port": 6379,
        "db": 1
    }
}

engine = None
session_factory = None
conf = None
inited = False
env1 = None

def init(env):
    global env1
    env1 = env
    global inited
    if inited:
        print "DB already inited", env
        return  ""
    print "DB initing....",env
    global engine
    global engine2
    global session_factory
    global session_factory2
    global conf
    conf = eval("db_" + env)
    engine = create_engine(conf["db_dining"], echo=False, pool_size=10, max_overflow=0, pool_recycle=3600)
    engine2 = create_engine(conf["db_connect_string"], echo=False, pool_size=10, max_overflow=0, pool_recycle=3600)
    session_factory = sessionmaker(bind=engine)
    session_factory2 = sessionmaker(bind=engine2)
    inited = True

def close():
    session_factory.close_all()

def sessionhandler(func):
    def wrapper(*args, **kwargs):
        try:
            ls = scoped_session(session_factory)
            kwargs["session"] = ls
            re = func(*args, **kwargs)
            ls.flush()
            ls.commit()
        except Exception,e:
            traceback.print_exc()
            ls.rollback()
            re = {"re": "500", "msg": str(e)}
        finally:
            ls.remove()
        return re
    return wrapper

def close2():
    session_factory2.close_all()

def sessionhandler2(func):
    def wrapper(*args, **kwargs):
        try:
            ls = scoped_session(session_factory2)
            kwargs["session"] = ls
            re = func(*args, **kwargs)
            ls.flush()
            ls.commit()
        except Exception,e:
            traceback.print_exc()
            ls.rollback()
            re = {"re": "500", "msg": str(e)}
        finally:
            ls.remove()
        return re
    return wrapper 