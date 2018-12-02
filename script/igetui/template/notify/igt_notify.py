class Notify():
    def __init__(self):
        self.title = None
        self.content = None
        self.payload = None
        self.type = None
        self.url=None
        self.intent=None

    def setTitle(self, title):
        self.title = title
    def getTitle(self):
        return self.title
    def setContent(self, content):
        self.content = content
    def getContent(self):
        return self.content
    def setPayload(self, payload):
        self.payload = payload
    def getPayload(self):
        return self.payload;
    def setType(self, type):
        self.type = type
    def getType(self):
        return self.type;
    def setUrl(self, url):
        self.url = url
    def getUrl(self):
        return self.url;
    def setIntent(self, intent):
        self.intent = intent
    def getIntent(self):
        return self.intent;
