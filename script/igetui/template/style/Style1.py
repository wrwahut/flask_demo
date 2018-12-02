from AbstractNotifyStyle import *
from protobuf.gt_req_pb2 import InnerFiled

class Style1(AbstractNotifyStyle):
    def __init__(self):
        AbstractNotifyStyle.__init__(self)
        self.text = ""
        self.title = ""
        self.logo = ""
        self.logoUrl = ""

    def getActionChain(self):
        title_F = self.actionChainBuilder.field.add()
        title_F.key = "title"
        title_F.val = self.title
        title_F.type = InnerFiled.string

        text_F = self.actionChainBuilder.field.add()
        text_F.key = "text"
        text_F.val = self.text
        text_F.type = InnerFiled.string

        text_F = self.actionChainBuilder.field.add()
        text_F.key = "logo"
        text_F.val = self.logo
        text_F.type = InnerFiled.string


        logo_F = self.actionChainBuilder.field.add()
        logo_F.key = "logo_url"
        logo_F.val = self.logoUrl
        logo_F.type = InnerFiled.string

        notifyStyle_F = self.actionChainBuilder.field.add()
        notifyStyle_F.key = "notifyStyle"
        notifyStyle_F.val = "1"
        notifyStyle_F.type = InnerFiled.string

        isRing_F = self.actionChainBuilder.field.add()
        isRing_F.key = "is_noring"
        isRing_F.val = str(self.isRing)
        isRing_F.type = InnerFiled.boolean

        isClearable_F = self.actionChainBuilder.field.add()
        isClearable_F.key = "is_noclear"
        isClearable_F.val = str(self.isClearable)
        isClearable_F.type = InnerFiled.boolean

        isVibrate_F = self.actionChainBuilder.field.add()
        isVibrate_F.key = "is_novibrate"
        isVibrate_F.val = str(self.isVibrate)
        isVibrate_F.type = InnerFiled.boolean
        return self.actionChainBuilder