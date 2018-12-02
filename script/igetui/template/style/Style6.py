# -*- coding: utf-8 -*-
from AbstractNotifyStyle import *
from protobuf.gt_req_pb2 import InnerFiled


class Style6(AbstractNotifyStyle):
    def __init__(self):
        AbstractNotifyStyle.__init__(self)
        self.text = ""
        self.title = ""
        self.logo = ""
        self.logoUrl = ""
        self.bigStyle = ""
        self.bigImageUrl = ""
        self.bigText = ""
        self.bannerUrl = ""
    def getActionChain(self):
        title_F = self.actionChainBuilder.field.add()
        title_F.key = "title"
        title_F.val = self.title
        title_F.type = InnerFiled.string

        text_F = self.actionChainBuilder.field.add()
        text_F.key = "text"
        text_F.val = self.text
        text_F.type = InnerFiled.string

        logo_F = self.actionChainBuilder.field.add()
        logo_F.key = "logo"
        logo_F.val = self.logo
        logo_F.type = InnerFiled.string

        logo_url_F = self.actionChainBuilder.field.add()
        logo_url_F.key = "logo_url"
        logo_url_F.val = self.logoUrl
        logo_url_F.type = InnerFiled.string

        notifyStyle_F = self.actionChainBuilder.field.add()
        notifyStyle_F.key = "notifyStyle"
        notifyStyle_F.val = "6"
        notifyStyle_F.type = InnerFiled.int32

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

        bigStyle_F = self.actionChainBuilder.field.add()
        bigStyle_F.key = "bigStyle"
        bigStyle_F.val = str(self.bigStyle)
        bigStyle_F.type = InnerFiled.int32
        if self.bigStyle is "1":
            bigImageUrl_F = self.actionChainBuilder.field.add()
            bigImageUrl_F.key = "big_image_url"
            bigImageUrl_F.val = self.bigImageUrl
            bigImageUrl_F.type = InnerFiled.string

        if self.bigStyle is "2":
            bigText_F = self.actionChainBuilder.field.add()
            bigText_F.key = "big_text"
            bigText_F.val = self.bigText
            bigText_F.type = InnerFiled.string
        if self.bigStyle is "3":
            bannerUrl_F = self.actionChainBuilder.field.add()
            bannerUrl_F.key = "banner_url"
            bannerUrl_F.val = self.bannerUrl
            bannerUrl_F.type = InnerFiled.string

            bigImageUrl_F = self.actionChainBuilder.field.add()
            bigImageUrl_F.key = "big_image_url"
            bigImageUrl_F.val = self.bigImageUrl
            bigImageUrl_F.type = InnerFiled.string

        return self.actionChainBuilder
