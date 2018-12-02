class SmsMessage:
    def __init__(self):
        self.smsTemplateId = None
        self.smsContent = dict()
        self.offlineSendtime = 0L
        self.url = None
        self.isApplink = False
        self.payload = None

    def setSmsTemplateId(self, smsTemplateId):
        self.smsTemplateId = smsTemplateId

    def getSmsTemplateId(self):
        return self.smsTemplateId

    def setSmsContent(self, smsContent):
        self.smsContent = smsContent

    def getSmsContent(self):
        return self.smsContent

    def setOfflineSendtime(self, offlineSendtime):
        self.offlineSendtime = offlineSendtime

    def getOfflineSendtime(self):
        return self.offlineSendtime;

    def setUrl(self, url):
        self.url = url

    def getUrl(self):
        return self.url;

    def setPayload(self, payload):
        self.payload = payload

    def getPayload(self):
        return self.payload;