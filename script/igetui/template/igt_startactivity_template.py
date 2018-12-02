from protobuf import *
import igt_base_template
import re
from GtConfig import *
from protobuf.gt_req_pb2 import InnerFiled
from igetui.template.style.AbstractNotifyStyle import *


class StartActivityTemplate(igt_base_template.BaseTemplate):
    def __init__(self):
        igt_base_template.BaseTemplate.__init__(self)
        self.intent = ""
        self.pattern = re.compile('^(intent:#Intent;).*(;end)$')
        self.transmissionContent = ""
        self.text = ""
        self.title = ""
        self.logo = ""
        self.logoURL = ""
        self.notifyStyle = 0
        self.isRing = True
        self.isVibrate = True
        self.isClearable = True
        self.pushType = "startmyactivity"
        self.style = None
        self.notifyid = 0

    def getActionChains(self):
        # set actionChain
        actionChain1 = gt_req_pb2.ActionChain()
        actionChain1.actionId = 1
        actionChain1.type = gt_req_pb2.ActionChain.Goto
        actionChain1.next = 10000
        # notification
        actionChain2 = gt_req_pb2.ActionChain()
        actionChain2.actionId = 10000
        actionChain2.type = gt_req_pb2.ActionChain.mmsinbox2
        actionChain2.stype = "notification"

        title_F = actionChain2.field.add()
        title_F.key = "title"
        title_F.val = self.title
        title_F.type = InnerFiled.string

        text_F = actionChain2.field.add()
        text_F.key = "text"
        text_F.val = self.text
        text_F.type = InnerFiled.string

        logo_F = actionChain2.field.add()
        logo_F.key = "logo"
        logo_F.val = self.logo
        logo_F.type = InnerFiled.string

        logo_url_F = actionChain2.field.add()
        logo_url_F.key = "logo_url"
        logo_url_F.val = self.logoURL
        logo_url_F.type = InnerFiled.string

        notifyStyle_F = actionChain2.field.add()
        notifyStyle_F.key = "notifyStyle"
        notifyStyle_F.val = str(self.notifyStyle)
        notifyStyle_F.type = InnerFiled.int32

        isRing_F= actionChain2.field.add()
        isRing_F.key = "is_noring"
        isRing_F.val = str(self.isRing)
        isRing_F.type = InnerFiled.boolean

        isClearable_F = actionChain2.field.add()
        isClearable_F.key = "is_noclear"
        isClearable_F.val = str(self.isClearable)
        isClearable_F.type = InnerFiled.boolean

        isVibrate_F = actionChain2.field.add()
        isVibrate_F.key = "is_novibrate"
        isVibrate_F.val = str(self.isVibrate)
        isVibrate_F.type = InnerFiled.boolean
        actionChain2.next = 10010

        actionChain3 = gt_req_pb2.ActionChain()
        actionChain3.actionId = 10010
        actionChain3.type = gt_req_pb2.ActionChain.Goto
        actionChain3.next = 11220
        if self.intent is not None:
            if len(self.intent) > GtConfig.getStartActivityIntentLimit():
                raise Exception('intent size overlimit')
            if not re.match(self.pattern, self.intent):
                raise Exception('intent format error,should start with "intent:#Intent;",end with ";end"->intent')
        actionChain4 = gt_req_pb2.ActionChain()
        actionChain4.actionId = 11220
        actionChain4.type = gt_req_pb2.ActionChain.mmsinbox2
        actionChain4.stype = self.pushType
        intent_F = actionChain4.field.add()
        intent_F.key = "uri"
        intent_F.val = self.intent
        intent_F.type = InnerFiled.string
        do_failed_F = actionChain4.field.add()
        do_failed_F.key = "do_failed"
        do_failed_F.val = "100"
        do_failed_F.type = InnerFiled.string
        actionChain4.next = 100

        actionChain5 = gt_req_pb2.ActionChain()
        actionChain5.actionId = 100
        actionChain5.type = gt_req_pb2.ActionChain.eoa

        actionChains = [actionChain1, actionChain2, actionChain3, actionChain4, actionChain5]
        return actionChains

    def getTemplateId(self):
            """templateid support,you do not need to call this function explicitly"""
            return 7








