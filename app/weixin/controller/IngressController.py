# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
from flask import Flask, Blueprint, request, render_template
from flask import jsonify, make_response, abort

app = Flask(__name__)

import os
from app.utils.MyLogger import MyLogger

logger = MyLogger.getLogger()

from app.weixin.serve.Basic import check_access_toke

cur_abs_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(cur_abs_dir)
templates_folder = os.path.join(os.path.dirname(root_dir), 'templates')

ingress = Blueprint('IngressController', __name__, url_prefix='/weixin')


class IngressController(object):
    pass


# def __init__(self):
#     pass

@ingress.route('/verify', methods=['GET'])
@check_access_toke
def POST():
    try:
        webData = request.args
        logger.info("Handle Post webdata is ", webData)
        '''
        recMsg = receive.parse_xml(webData)
        if isinstance(recMsg, receive.Msg):
            toUser = recMsg.FromUserName
            fromUser = recMsg.ToUserName
            if recMsg.MsgType == 'text':
                content = recMsg.Content
                print "返回的数据为：", content
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            if recMsg.MsgType == 'image':
                mediaId = recMsg.MediaId
                print "返回的数据mediaId为：", mediaId
                replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                return replyMsg.send()
            else:
                return reply.Msg().send()
        else:
            print "暂且不处理"
            return reply.Msg().send()
        '''
    except Exception, Argment:
        return Argment


@ingress.route('/', methods=['GET'])
def GET():
    logger.info('开始进行验证！')
    try:
        data = request.args.items()
        if len(data) == 0:
            return "data is null! plase cheking"

        data = request.args
        signature = data.get('signature', '')
        timestamp = data.get('timestamp', '')
        nonce = data.get('nonce', '')
        echostr = data.get('echostr', '')

        token = "mianduixianshi19921223"

        list = [token, timestamp, nonce]
        list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, list)
        hashcode = sha1.hexdigest()

        if hashcode == signature:
            return make_response(echostr)
        else:
            return ""

    except Exception as Argument:
        return Argument


'''
-1      系统繁忙，此时请开发者稍候再试
0       请求成功
40001   AppSecret错误或者AppSecret不属于这个公众号，请开发者确认AppSecret的正确性
40002   请确保grant_type字段值为client_credential
40164   调用接口的IP地址不在白名单中，请在接口IP白名单中进行设置

'''
