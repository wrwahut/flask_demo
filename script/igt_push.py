# -*- coding: utf-8 -*-
import cookielib

__author__ = 'wei'

import StringIO
import gzip
import hashlib
# import urllib2
import threading

import requests

from BatchImpl import *
from RequestException import RequestException
from igetui.igt_message import *
from igetui.utils.igt_lang_utils import LangUtils

globals = {
    'false': "false",
    'true': "true",
    'null': "null"
}


class IGeTui:
    serviceMap = dict()
    session = requests.session()
    def __init__(self, host, appKey, masterSecret, ssl=None):
        self.appKey = appKey
        self.masterSecret = masterSecret
        self.authToken = ""
        if host is not None:
            host = host.strip()

        if ssl is None and host is not None and host != '' and host.lower().startswith('https:'):
            ssl = True

        self.useSSL = (ssl if ssl is not None else False)
        if host is None or len(host) <= 0:
            self.hosts = GtConfig.getDefaultDomainUrl(self.useSSL)
        else:
            self.hosts = list()
            self.hosts.append(host)
        self.initOSDomain()

    def initOSDomain(self):

        hosts = IGeTui.serviceMap.get(self.appKey)
        # 第一次创建时要获取域名列表同时启动检测线程
        if hosts is None or len(hosts) == 0:
            hosts = self.getOSPushDomainUrlList()
            IGeTui.serviceMap[self.appKey] = hosts
            self.getFastUrl()

    def getOSPushDomainUrlList(self):
        postData = dict()
        postData['action'] = 'getOSPushDomailUrlListAction'
        postData['appkey'] = self.appKey
        ex = None
        for host in self.hosts:
            try:
                response = self.httpPostJson(host, postData)
                if response is not None and response['result'] == 'ok':
                    return response['osList']
            except Exception as e:
                ex = e
        raise Exception("Can not get hosts from " + str(self.hosts), ex)

    def getFastUrl(self, hosts=None):
        if hosts is None:
            self.cycleInspect()
        mint = 30.0
        s_url = ""
        for host in IGeTui.serviceMap[self.appKey]:
            s = time.time()
            if GtConfig.getHttpProxyIp() is not None:
                # 配置代理如下
                userAndPass = "%s:%s" % (GtConfig.getHttpProxyUserName(), GtConfig.getHttpProxyPasswd())
                ipport = "%s:%s" % (GtConfig.getHttpProxyIp(), GtConfig.getHttpProxyPort())
                http_proxy = "http://" + userAndPass + "@" + ipport + "/"
                https_proxy = "http://" + userAndPass + "@" + ipport + "/"
                proxies = {
                    "http": http_proxy,
                    "https": https_proxy
                }
                self.session.post(host, proxies=proxies, timeout=GtConfig.getHttpConnectionTimeOut(), stream=False, verify=True)
            else:
                self.session.post(host, timeout=GtConfig.getHttpConnectionTimeOut(), stream=False, verify=True)
            pass
            e = time.time()
            diff = e - s
            print host, diff
            if mint > diff:
                mint = diff
                s_url = host
        if s_url != "":
            self.host = s_url

    def cycleInspect(self):
        if len(IGeTui.serviceMap[self.appKey]) == 0:
            raise ValueError("can't get fastest host from empty list")
        else:
            t = threading.Timer(GtConfig.getHttpInspectInterval(), self.getFastUrl)
            t.setDaemon(True)
            t.start()

    def connect(self):
        timestamp = self.getCurrentTime()
        sign = self.getSign(self.appKey, timestamp, self.masterSecret)
        params = dict()
        params['action'] = 'connect'
        params['appkey'] = self.appKey
        params['timeStamp'] = timestamp
        params['sign'] = sign
        params['version'] = GtConfig.getSDKVersion()
        rep = self.httpPost(self.host, params)

        if 'success' == (rep['result']):
            if rep.has_key('authtoken'):
                self.authToken = rep['authtoken']
            return True

        raise Exception(str(rep) + "appKey or masterSecret is auth failed.")

    def getBatch(self):
        return BatchImpl(self, self.appKey, self)

    def pushMessageToSingle(self, message, target, requestId=None):
        params = dict()
        if requestId is None:
            requestId = str(uuid.uuid1())
        params['requestId'] = requestId
        params['action'] = "pushMessageToSingleAction"
        params['appkey'] = self.appKey
        transparent = message.data.getTransparent()
        params['clientData'] = base64.encodestring(transparent.SerializeToString())
        params['transmissionContent'] = message.data.transmissionContent
        params['isOffline'] = message.isOffline
        params['offlineExpireTime'] = message.offlineExpireTime
        # 增加pushNetWorkType参数(0:不限;1:wifi;2:4G/3G/2G)
        params["pushNetWorkType"] = message.pushNetWorkType
        params['appId'] = target.appId
        params['clientId'] = target.clientId
        params['alias'] = target.alias
        params['type'] = 2  # default is message
        params['pushType'] = message.data.pushType

        return self.httpPostJson(self.host, params)

    def pushAPNMessageToSingle(self, appId, deviceToken, message):
        if deviceToken is None or len(deviceToken) != 64:
            raise Exception("deviceToken " + deviceToken + " length must be 64.")
        params = dict()
        params['action'] = "apnPushToSingleAction"
        params['appId'] = appId
        params['appkey'] = self.appKey
        params['DT'] = deviceToken
        params['PI'] = base64.encodestring(message.data.pushInfo.SerializeToString())

        return self.httpPostJson(self.host, params)

    def pushMessageToApp(self, message, taskGroupName=None):
        params = dict()
        contentId = self.getContentId(message, taskGroupName)
        params['action'] = "pushMessageToAppAction"
        params['appkey'] = self.appKey
        params['contentId'] = contentId
        params['type'] = 2
        return self.httpPostJson(self.host, params)

    def pushMessageToList(self, contentId, targets):
        params = dict()
        params['action'] = 'pushMessageToListAction'
        params['appkey'] = self.appKey
        params['contentId'] = contentId
        needDetails = GtConfig.isPushListNeedDetails()
        params['needDetails'] = GtConfig.isPushListNeedDetails()
        async = GtConfig.isPushListAsync()
        params["async"] = async

        if async and not needDetails:
            limit = GtConfig.getAsyncListLimit()
        else:
            limit = GtConfig.getSyncListLimit()

        if len(targets) > limit:
            raise AssertionError("target size:" + str(len(targets)) + " beyond the limit:" + str(limit))

        clientIdList = []
        aliasList = []
        appId = ''
        for target in targets:
            clientId = target.clientId.strip()
            alias = target.alias.strip()
            if clientId != '':
                clientIdList.append(clientId)
            elif alias != '':
                aliasList.append(alias)

            if appId == '':
                appId = target.appId.strip()

        params['appId'] = appId
        params['clientIdList'] = clientIdList
        params['aliasList'] = aliasList
        params['type'] = 2
        return self.httpPostJson(self.host, params, True)

    def pushAPNMessageToList(self, appId, contentId, deviceTokenList):
        for deviceToken in deviceTokenList:
            if deviceToken is None or len(deviceToken) != 64:
                raise Exception("deviceToken " + deviceToken + " length must be 64.")

        params = dict()
        params['action'] = "apnPushToListAction"
        params['appkey'] = self.appKey
        params['appId'] = appId
        params['contentId'] = contentId
        params['DTL'] = deviceTokenList
        params['needDetails'] = GtConfig.isPushListNeedDetails()
        params['async'] = GtConfig.isPushListAsync()

        return self.httpPostJson(self.host, params)

    def close(self):
        params = dict()
        params['action'] = 'close'
        params['appkey'] = self.appKey
        params['version'] = GtConfig.getSDKVersion()
        params['authToken'] = self.authToken
        self.httpPostJson(self.host, params)

    def stop(self, contentId):
        params = dict()
        params['action'] = 'stopTaskAction'
        params['appkey'] = self.appKey
        params['contentId'] = contentId

        ret = self.httpPostJson(self.host, params)
        if ret["result"] == 'ok':
            return True
        return False

    def getClientIdStatus(self, appId, clientId):
        params = dict()
        params['action'] = 'getClientIdStatusAction'
        params['appkey'] = self.appKey
        params['appId'] = appId
        params['clientId'] = clientId

        return self.httpPostJson(self.host, params)

    def bindAlias(self, appId, alias, clientId):
        params = dict()
        params['action'] = 'alias_bind'
        params['appkey'] = self.appKey
        params['appid'] = appId
        params['alias'] = alias
        params['cid'] = clientId

        return self.httpPostJson(self.host, params)

    def bindAliasBatch(self, appId, targetList):
        params = dict()
        aliasList = []
        for target in targetList:
            user = dict()
            user['cid'] = target.clientId
            user['alias'] = target.alias
            aliasList.append(user)

        params['action'] = 'alias_bind_list'
        params['appkey'] = self.appKey
        params['appid'] = appId
        params['aliaslist'] = aliasList

        return self.httpPostJson(self.host, params)

    def queryClientId(self, appId, alias):
        params = dict()
        params['action'] = "alias_query"
        params['appkey'] = self.appKey
        params['appid'] = appId
        params['alias'] = alias

        return self.httpPostJson(self.host, params)

    def queryAlias(self, appId, clientId):
        params = dict()
        params['action'] = "alias_query"
        params['appkey'] = self.appKey
        params['appid'] = appId
        params['cid'] = clientId

        return self.httpPostJson(self.host, params)

    def unBindAlias(self, appId, alias, clientId=None):
        params = dict()
        params['action'] = "alias_unbind"
        params['appkey'] = self.appKey
        params['appid'] = appId
        params['alias'] = alias

        if clientId is not None and clientId.strip() != "":
            params['cid'] = clientId
        return self.httpPostJson(self.host, params)

    def unBindAliasAll(self, appId, alias):
        return self.unBindAlias(appId, alias, None)

    def getContentId(self, message, taskGroupName=None):
        params = dict()

        if taskGroupName is not None and taskGroupName.strip() != "":
            if len(taskGroupName) > 40:
                raise Exception("TaskGroupName is OverLimit 40")
            params['taskGroupName'] = taskGroupName

        params['action'] = "getContentIdAction"
        params['appkey'] = self.appKey
        transparent = message.data.getTransparent()
        params['clientData'] = base64.encodestring(transparent.SerializeToString())
        params['transmissionContent'] = message.data.transmissionContent
        params["isOffline"] = message.isOffline
        params["offlineExpireTime"] = message.offlineExpireTime
        # 增加pushNetWorkType参数(0:不限;1:wifi;2:4G/3G/2G)
        params["pushNetWorkType"] = message.pushNetWorkType
        params["pushType"] = message.data.pushType
        params['type'] = 2

        if isinstance(message, IGtListMessage):
            params['contentType'] = 1
        elif isinstance(message, IGtAppMessage):
            personaTags = []
            if message.getConditions() is None:
                params['phoneTypeList'] = message.getPhoneTypeList()
                params['provinceList'] = message.getProvinceList()
                params['tagList'] = message.getTagList()

            else:
                conditions = message.getConditions().getCondition()
                params['conditions'] = conditions

            params['speed'] = message.speed
            params['contentType'] = 2
            params['appIdList'] = message.appIdList
            if message.getPushTime() is not None and message.getPushTime() is not "":
                params['pushTime'] = message.getPushTime()

        ret = self.httpPostJson(self.host, params)
        if "ok" == ret.get('result'):
            return ret['contentId']
        else:
            raise Exception("获取 contentId 失败：" + ret)

    def getAPNContentId(self, appId, message):
        params = dict()
        params['action'] = "apnGetContentIdAction"
        params['appkey'] = self.appKey
        params['appId'] = appId
        params['PI'] = base64.encodestring(message.data.pushInfo.SerializeToString())

        ret = self.httpPostJson(self.host, params)
        if "ok" == ret.get('result'):
            return ret['contentId']
        else:
            raise Exception("获取 contentId 失败：" + ret)

    def cancelContentId(self, contentId):
        params = dict()
        params['action'] = 'cancleContentIdAction'
        params['appkey'] = self.appKey
        params['contentId'] = contentId
        ret = self.httpPostJson(self.host, params)
        return True if ret.get('result') == 'ok' else False

    def getCurrentTime(self):
        return int(time.time() * 1000)

    def getSign(self, appKey, timeStamp, masterSecret):
        rawValue = appKey + str(timeStamp) + masterSecret
        return hashlib.md5(rawValue.encode()).hexdigest()

    def httpPostJson(self, host, params, needGzip=False):
        params['version'] = GtConfig.getSDKVersion()
        params['authToken'] = self.authToken
        ret = self.httpPost(host, params, needGzip)
        if ret is None or ret == '':
            if params.get('requestId') is not None:
                raise RequestException(params['requestId'])
            return ret
        if 'sign_error' == ret['result']:
            if self.connect():
                params['authToken'] = self.authToken
                ret = self.httpPostJson(host, params, needGzip)
        elif 'domain_error' == ret['result']:
            IGeTui.serviceMap[self.appKey] = ret['osList']
            self.getFastUrl(ret['osList'])
            ret = self.httpPostJson(self.host, params)
        return ret

    def httpPost(self, host, params, needGzip=False):
        headers = dict()
        data_json = json.dumps(params)
        headers['Gt-Action'] = params.get("action")
        if needGzip:
            out = StringIO.StringIO()
            with gzip.GzipFile(fileobj=out, mode="w") as f:
                f.write(data_json)
            data_json = out.getvalue()
            headers['Content-Encoding'] = 'gzip'
            headers['Accept-Encoding'] = 'gzip'

        retry_time_limit = GtConfig.getHttpTryCount()
        isFail = True
        tryTime = 0
        res_stream = None

        while isFail and tryTime < retry_time_limit:
            if GtConfig.getHttpProxyIp() is not None:
                # 配置代理如下
                userAndPass = "%s:%s" % (GtConfig.getHttpProxyUserName(), GtConfig.getHttpProxyPasswd())
                ipport = "%s:%s" % (GtConfig.getHttpProxyIp(), GtConfig.getHttpProxyPort())
                http_proxy = "http://" + userAndPass + "@" + ipport + "/"
                https_proxy = "http://" + userAndPass + "@" + ipport + "/"
                proxies = {
                    "http": http_proxy,
                    "https": https_proxy
                }
                res_stream = self.session.post(host, proxies=proxies, data=data_json, headers=headers, timeout=GtConfig.getHttpConnectionTimeOut(),
                                verify=True, stream=False)
            else:
                res_stream = self.session.post(host, data=data_json, headers=headers,
                                               timeout=GtConfig.getHttpConnectionTimeOut(),
                                               verify=True, stream=False)
            isFail = False
            tryTime += 1

        if res_stream is None:
            return None
        page_str = res_stream.text
        if needGzip:
            compressedstream = StringIO.StringIO(page_str)
            # requests自动解压文件
            # with gzip.GzipFile(fileobj=compressedstream) as f:
            data = compressedstream.read()
            return json.loads(data)
        else:
            return eval(page_str, globals)

    def getPushResult(self, taskId):
        params = dict()
        params["action"] = "getPushMsgResult"
        params["appkey"] = self.appKey
        params["taskId"] = taskId

        return self.httpPostJson(self.host, params)

    def getPushResultByGroupName(self, appId, groupName):
        params = dict()
        params["action"] = "getPushResultByGroupName"
        params["appkey"] = self.appKey
        params["appId"] = appId
        params["groupName"] = groupName

        return self.httpPostJson(self.host, params)

    def getLast24HoursOnlineUserStatistics(self, appId):
        params = dict()
        params["action"] = "getLast24HoursOnlineUser"
        params["appkey"] = self.appKey
        params["appId"] = appId
        return self.httpPostJson(self.host, params)

    def getUserTags(self, appId, clientId):
        params = dict()
        params["action"] = "getUserTags"
        params["appkey"] = self.appKey
        params["appId"] = appId
        params["clientId"] = clientId
        return self.httpPostJson(self.host, params)

    def getPersonaTags(self, appId):
        params = dict()
        params["action"] = "getPersonaTags"
        params["appkey"] = self.appKey
        params["appId"] = appId
        return self.httpPostJson(self.host, params)

    def queryUserCount(self, appId, conditions):
        params = dict()
        params["action"] = "queryUserCount"
        params["appId"] = appId
        params["appkey"] = self.appKey
        # token
        if conditions is not None:
            params["conditions"] = conditions.getCondition()
        return self.httpPostJson(self.host, params)

    def setClientTag(self, appId, clientId, tags):
        params = dict()
        params["action"] = "setTagAction"
        params["appkey"] = self.appKey
        params["appId"] = appId
        params["clientId"] = clientId
        params["tagList"] = tags
        return self.httpPostJson(self.host, params)

    def queryAppPushDataByDate(self, appId, date):
        if LangUtils.validateDate(date) == False:
            raise ValueError("DateError|" + date)
        params = dict()
        params["action"] = "queryAppPushData"
        params["appkey"] = self.appKey
        params["appId"] = appId
        params["date"] = date
        return self.httpPostJson(self.host, params)

    def queryAppUserDataByDate(self, appId, date):
        if LangUtils.validateDate(date) == False:
            raise ValueError("DateError|" + date)
        params = dict()
        params["action"] = "queryAppUserData"
        params["appkey"] = self.appKey
        params["appId"] = appId
        params["date"] = date
        return self.httpPostJson(self.host, params)

    def blackCidList(self, appId, cidList, optType):
        params = dict()
        limit = GtConfig.getMaxLenOfBlackCidList()
        if limit < len(cidList):
            raise OverflowError("cid size:" + len(cidList) + " beyond the limit:" + limit)
        params["action"] = "blackCidAction"
        params["appkey"] = self.appKey
        params["appId"] = appId
        params["cidList"] = cidList
        params["optType"] = optType
        return self.httpPostJson(self.host, params)

    def addCidListToBlk(self, appId, cidList):
        return self.blackCidList(appId, cidList, 1)

    def restoreCidListFromBlk(self, appId, cidList):
        return self.blackCidList(appId, cidList, 2)

    def setBadgeForCID(self, badge, appid, cidList):
        return self.setBadge(badge, appid, list(), cidList);

    def setBadgeForDeviceToken(self, badge, appid, deviceTokenList):
        return self.setBadge(badge, appid, deviceTokenList, list());

    def setBadge(self, badge, appid, deviceTokenList, cidList):
        params = dict()
        params["action"] = "setBadgeAction"
        params["appkey"] = self.appKey
        params["badge"] = badge
        params["appid"] = appid
        params["deviceToken"] = deviceTokenList
        params["cid"] = cidList
        return self.httpPostJson(self.host, params)

    def getPushResultByTaskidList(self, taskIdList):
        return self.getPushActionResultByTaskids(taskIdList, None)

    def getPushActionResultByTaskids(self, taskIdList, actionIdList):
        params = dict()
        params["action"] = "getPushMsgResultByTaskidList"
        params["appkey"] = self.appKey
        params["taskIdList"] = taskIdList
        params["actionIdList"] = actionIdList
        return self.httpPostJson(self.host, params)

    def pushTagMessage(self, message, requestId):
        if requestId is None or requestId.strip() is "":
            requestId = str(uuid.uuid1())
        params = dict()
        params["action"] = "pushMessageByTagAction"
        params["appkey"] = self.appKey
        transparent = message.data.getTransparent()
        params['clientData'] = base64.encodestring(transparent.SerializeToString())
        params['transmissionContent'] = message.data.transmissionContent
        params['isOffline'] = message.isOffline
        params['offlineExpireTime'] = message.offlineExpireTime
        params['isOffline'] = message.isOffline
        # 增加pushNetWorkType参数(0:不限;1:wifi;2:4G/3G/2G)
        params["pushNetWorkType"] = message.pushNetWorkType
        params["appIdList"] = message.appIdList
        params["speed"] = message.speed
        params["requestId"] = requestId
        params["tag"] = message.tag
        return self.httpPostJson(self.host, params)

    def pushTagMessageRetry(self, message):
        return self.pushTagMessage(message, None)

    def getScheduleTask(self, taskId, appId):
        params = dict()
        params["action"] = "getScheduleTaskAction"
        params["appId"] = appId
        params["appkey"] = self.appKey
        params["taskId"] = taskId
        return self.httpPostJson(self.host, params)

    def delScheduleTask(self, taskId, appId):
        params = dict()
        params["action"] = "delScheduleTaskAction"
        params["appId"] = appId
        params["appkey"] = self.appKey
        params["taskId"] = taskId
        return self.httpPostJson(self.host, params)

    def bindCidPn(self, appId, cidAndPn):
        params = dict()
        params["action"] = "bind_cid_pn"
        params["appId"] = appId
        params["appkey"] = self.appKey
        params["cidpnlist"] = cidAndPn
        return self.httpPostJson(self.host, params)

    def unbindCidPn(self, appId, cid):
        params = dict()
        params["action"] = "unbind_cid_pn"
        params["appId"] = appId
        params["appkey"] = self.appKey
        params["cids"] = cid
        return self.httpPostJson(self.host, params)

    def queryCidPn(self, appId, cid):
        params = dict()
        params["action"] = "query_cid_pn"
        params["appId"] = appId
        params["appkey"] = self.appKey
        params["cids"] = cid
        return self.httpPostJson(self.host, params)

    def stopSendSms(self, appId, taskId):
        params = dict()
        params["action"] = "stop_sms"
        params["appId"] = appId
        params["appkey"] = self.appKey
        params["taskId"] = taskId
        return self.httpPostJson(self.host, params)

    def getUserCountByTags(self, appId, tagList):
        params = dict()
        params["action"] = "getUserCountByTags"
        params["appkey"] = self.appKey
        params["appId"] = appId
        params["tagList"] = tagList
        limit = GtConfig.getTagListLimit()
        if len(tagList) > limit:
            raise Exception("tagList size:" + len(tagList) + "beyond the limit" + limit)
        return self.httpPostJson(self.host, params)

    def getAuthToken(self):
        return self.authToken
