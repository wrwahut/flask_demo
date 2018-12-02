import json
class VoIPPayload:
    def __init__(self):
        self.voIPPayload = ""
    def getPayload(self):
        payload = self.voIPPayload
        if payload is None or payload == '':
            raise RuntimeError("payload cannot be empty")
        params = dict()
        if payload is not None:
            params['payload'] = payload
        params['isVoIP'] = 1
        return  json.dumps(params)
    def setVoIPPayload(self, voIPPayload):
        self.voIPPayload = voIPPayload

