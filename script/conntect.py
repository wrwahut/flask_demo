# -*- coding:utf-8 -*-
import requests
from flask import request
import json

req_session = requests.session()

class Caller(object):

    def __init__(self, url_fix,args={}):
        self.url = "http://localhost:10002/resource/user/" + url_fix
        self.args = args
        self.headers = {
            "content-type": "application/json",
            "accept": "application/json"
        }
        # self.cookie = {
        #     "token": request.cookies.get("token", "None"),
        #     "lang": request.cookies.get("lang", "zh-CN")
        # }

    def _res_data(self, response):
        res_data = response.json()
        if not res_data.get("data"):
            res_data["data"] = {}
        return res_data
    
    def post_req(self):
        payload = json.dumps(self.args, "utf-8")
        response = req_session.post(self.url, data=payload, headers=self.headers)
        return self._res_data(response)