# -*- coding:utf-8 -*-

import sys
import gunicorn.app.base
from gunicorn.six import iteritems
from backend.app import create_app
from backend.config.LocalConfig import local

def handler_app():
    return create_app(config=local())

def get_options():
    return {
        "bind": "0.0.0.0:10002",
        "workers": 4,
        "worker_class": "gevent"
    }

class StandloneApp(gunicorn.app.base.BaseApplication):
    
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandloneApp, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options) if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

if __name__ == "__main__":
    StandloneApp(handler_app(), get_options()).run()