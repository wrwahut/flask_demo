from flask import current_app
from backend.extensions import redis

class Redisi(object):

    def __init__(self):
        self.r = redis

    def get_data(self, key):
        return self.r.get(key)

    def set_data(self, key, value, expire=None):
        if expire:
            self.r.set(key, value,  expire)
        else:
            self.r.set(key, value)
        return True

    def del_data(self, key):
        self.r.delete(key)
        return True
    
    def check(self, key, value, check=False):
        res = self.get_data(key)
        if res:
            if res == value:
                if not check:
                    self.del_data(key)
                return True
        return False