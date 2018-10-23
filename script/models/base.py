# -*- coding:utf-8 -*-

import  time
import uuid

class CRUD(object):
    def init(self, data={}, session=None):
        if hasattr(self, "ctime"):
            self.ctime = int(time.time())
        if hasattr(self, "uuid"):
            self.uuid =  "a" + str(uuid.uuid1()).replace("-","")
        self.change_data(data)
        session.add(self)

    def change_data(self, data={}):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        if hasattr(self, "utime"):
            self.utime = int(time.time())

    def delete(self):
        session.delete(self)