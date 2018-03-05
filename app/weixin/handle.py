# -*- coding: utf-8 -*-
# filename: handle.py
from flask import Flask, jsonify
from flask import request, make_response
from flask import abort
import hashlib

app = Flask(__name__)

from flask import Blueprint, render_template
import os
from app.utils.MyLogger import MyLogger

logger = MyLogger.getLogger()

from app.weixin.basic import check_access_toke

cur_abs_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(cur_abs_dir)
templates_folder = os.path.join(os.path.dirname(root_dir), 'templates')

handle = Blueprint('handle', __name__, url_prefix='/weixin')


class Handle(object):
    pass


# def __init__(self):
#     pass


@handle.route('/verify', methods=['GET', 'POST'])
@check_access_toke
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
        logger.info(echostr)
        if hashcode == signature:
            return make_response(echostr)
        else:
            return ""

    except Exception as Argument:
        return Argument


'''
def POST(self):
    try:
        webData = web.data()
        print "Handle Post webdata is ", webData  # 后台打日志
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
    except Exception, Argment:
        return Argment
'''
