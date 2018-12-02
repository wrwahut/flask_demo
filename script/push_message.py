# -*- coding: utf-8 -*-
__author__ = 'wei'
from igt_push import *
from igetui.template import *
from igetui.template.igt_base_template import *
from igetui.template.igt_transmission_template import *
from igetui.template.igt_link_template import *
from igetui.template.igt_notification_template import *
from igetui.template.igt_notypopload_template import *
from igetui.igt_message import *
from igetui.igt_target import *
from igetui.template import *

APPKEY = "wYw2rEacQhA1SkakK9p9x4"
APPID = "QwzLKUfDts7woiM0P26U59"
MASTERSECRET = "v4HqPlkihgAROu3nTXi7wA"
CID = "8713dd61d415c9806bd3d3f3716a0293"

HOST = 'http://sdk.open.api.igexin.com/apiex.htm'

push = IGeTui(HOST, APPKEY, MASTERSECRET)

def pushMessageToSingle(CID, push_data):
    # push = IGeTui(HOST, APPKEY, MASTERSECRET)
    template = TransmissionTemplateDemo(push_data)
    message = IGtSingleMessage()
    message.isOffline = True
    message.offlineExpireTime = 1000 * 3600 * 12
    message.data = template
    message.pushNetWorkType = 0 #设置是否根据WIFI推送消息，2为4G/3G/2G,1为wifi推送，0为不限制推送
    target = Target()
    target.appId = APPID
    target.clientId = CID
    #target.alias = ALIAS

    try:
        ret = push.pushMessageToSingle(message, target)
        print ret
    except RequestException, e:
        # 发生异常重新发送
        requstId = e.getRequestId()
        ret = push.pushMessageToSingle(message, target, requstId)
        print ret
    push.close()

#透传模板动作内容
def TransmissionTemplateDemo(push_data):
    template = TransmissionTemplate()
    template.transmissionType = 1
    template.appId = APPID
    template.appKey = APPKEY
    template.transmissionContent = push_data
    return template

# pushMessageToSingle(CID,{"name": "wrw"})