# -*- coding: utf-8 -*-
from protobuf import *
from igetui.template.style.INotifyStyle import *
class AbstractNotifyStyle(INotifyStyle):
    def __init__(self):
        self.isRing = True
        self.isVibrate = True
        self.isClearable = True
        actionChainBuilder = gt_req_pb2.ActionChain()
        actionChainBuilder.actionId = 10000
        actionChainBuilder.type = gt_req_pb2.ActionChain.mmsinbox2
        actionChainBuilder.stype = "notification"
        actionChainBuilder.next = 10010
        self.actionChainBuilder = actionChainBuilder
