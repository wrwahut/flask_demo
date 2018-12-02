# -*- coding: utf-8 -*-

import time

from igetui.template.notify.igt_smsmessage import SmsMessage
from protobuf import *
from payload.APNPayload import APNPayload, DictionaryAlertMsg
from protobuf.gt_req_pb2 import SmsInfo


class BaseTemplate:
    def __init__(self):
        self.appKey = ""
        self.appId = ""
        self.pushInfo = gt_req_pb2.PushInfo()
        self.pushInfo.invalidAPN = True
        self.pushInfo.invalidMPN = True
        self.duration = 0
        self.smsInfo = None
        
    def getTransparent(self):
        transparent = gt_req_pb2.Transparent()
        transparent.id = ""
        transparent.templateId = self.getTemplateId()
        transparent.action = "pushmessage"
        transparent.taskId = ""
        transparent.appKey = self.appKey
        transparent.appId = self.appId
        transparent.messageId = ""
        transparent.pushInfo.CopyFrom(self.getPushInfo())
        if self.smsInfo is not None:
            transparent.smsInfo.CopyFrom(self.smsInfo)

        actionChains = self.getActionChains()        
        for actionChain in actionChains:
            tmp = transparent.actionChain.add()
            tmp.CopyFrom(actionChain)           
        # add condition
        transparent.condition.append(self.getDurCondition())            
        return transparent
        
    def getActionChains(self):
        return []

    def getPushInfo(self):
        return self.pushInfo

    def setApnInfo(self, payload):
        if payload is None:
            return
        payload = payload.getPayload()
        if payload is None or payload is "":
            return
        length = len(payload)
        if length > APNPayload.PAYLOAD_MAX_BYTES:
            raise Exception("APN payload length overlength (" + str(length) + ">"
                            + str(APNPayload.PAYLOAD_MAX_BYTES) + ")")

        self.pushInfo.apnJson = payload
        self.pushInfo.invalidAPN = False

    def setPushInfo(self, actionLocKey, badge, message, sound, payload, locKey, locArgs, launchImage,
                    contentAvailable=0):

        self.pushInfo = gt_req_pb2.PushInfo()
        self.pushInfo.invalidAPN = True
        self.pushInfo.invalidMPN = True
        
        alertMsg = DictionaryAlertMsg()
        if locKey is not None and locKey is not "":
            alertMsg.locKey = locKey.decode("utf-8")
        if locArgs is not None and locArgs is not "":
            alertMsg.locArgs.append(locArgs.decode("utf-8"))
        if actionLocKey is not None and actionLocKey is not "":
            alertMsg.actionLocKey = actionLocKey.decode("utf-8")
        if message is not None and message is not "":
            alertMsg.body = message.decode("utf-8")
        if launchImage is not None and launchImage is not "":
            alertMsg.launchImage = launchImage.decode("utf-8")
        
        apn = APNPayload()
        apn.alertMsg = alertMsg
        if badge is not None:
            alertMsg.badge = badge
        if sound is not None and sound is not "":
            apn.sound = sound.decode("utf-8")
        if contentAvailable is not None:
            apn.contentAvailable = contentAvailable
        if payload is not None and payload is not "":
            apn.addCustomMsg("payload", payload.decode("utf-8"))
            
        self.setApnInfo(apn)

    def setSmsInfo(self, smsMessage):
        if smsMessage is None:
            raise RuntimeError("smsInfo cannot be empty")
        else:
            smsTemplateId = smsMessage.smsTemplateId
            smsContent = smsMessage.smsContent
            offlineSendtime = smsMessage.offlineSendtime
            smsSendDuration = 0L
            if(smsTemplateId is not None and smsTemplateId is not ""):
                if offlineSendtime is None:
                    raise RuntimeError("offlineSendtime cannot be empty")
                else:
                    build = gt_req_pb2.SmsInfo()
                    build.smsChecked = False
                    build.smsTemplateId = smsTemplateId
                    build.offlineSendtime = offlineSendtime
                    if smsMessage.isApplink is True:
                        if smsContent != None and smsContent.has_key("url"):
                            raise RuntimeError("SmsContent cann not contains key about url")
                        smsContentEntry = build.smsContent.add()
                        smsContentEntry.key = "applinkIdentification"
                        smsContentEntry.value = "1"
                        payload = smsMessage.payload
                        if payload is not None and payload is not "":
                            smsContentEntry = build.smsContent.add()
                            smsContentEntry.key = "url"
                            if smsMessage.url is not None:
                                smsContentEntry.value = smsMessage.url + "?n=" + payload + "&p="
                            else:
                                raise RuntimeError("smsMessage must  contains key about url")
                        else:
                            smsContentEntry = build.smsContent.add()
                            smsContentEntry.key = "url"
                            if smsMessage.url is not None:
                                smsContentEntry.value = smsMessage.url + "?p="
                            else:
                                raise RuntimeError("smsMessage must  contains key about url")
                    if smsContent is not None:
                        for key, value in smsContent.items():
                            if key is None or key is "" or value is None:
                                raise RuntimeError("smsContent entry cannot be null")
                            else:
                                smsContentEntry = build.smsContent.add()
                                smsContentEntry.key = key
                                smsContentEntry.value = value
                    if smsSendDuration is not None:
                        build.smsSendDuration = smsSendDuration

                    self.smsInfo = build
            else:
                raise RuntimeError("smsTemplateId cannot be empty")


    def getDurCondition(self):
        if self.duration != 0 and len(self.duration) > 0:
            return "duration=" + str(self.getDuration())
        else:
            return ""
    
    def getDuration(self):
            return self.duration

    def setDuration(self, begin, end):
        s = long(time.mktime(time.strptime(begin, "%Y-%m-%d %H:%M:%S")) * 1000)
        e = long(time.mktime(time.strptime(end, "%Y-%m-%d %H:%M:%S")) * 1000)
        if s <= 0 or e <= 0:
            raise ValueError("DateFormat: yyyy-MM-dd HH:mm:ss")
        if s > e:
            raise ValueError("startTime should be smaller than endTime")
        self.duration = str(s) + "-" + str(e)

    def getTemplateId(self):
        """templateid support,you do not need to call this function explicitly"""
        return -1