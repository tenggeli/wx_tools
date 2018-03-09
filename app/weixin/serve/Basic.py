# -*- coding: utf-8 -*-
#  filename: basic.py

import os, time, urllib, json
from flask import Flask, Blueprint, request
from flask import jsonify, abort, render_template
from functools import wraps

app = Flask(__name__)

from app.models.wx_tools.accessToken import accessToken

from app.utils.MyLogger import MyLogger

logger = MyLogger.getLogger()

cur_abs_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(cur_abs_dir)


# basic = Blueprint('Basic', __name__)

class Basic:
    '''
        classdocs
    '''


def __real_get_access_token():
    appId = "wxe2b38dabbb686f21"
    appSecret = "8e511b955bab52120e2f821684ea7859"

    postUrl = (
        "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (appId, appSecret))
    urlResp = urllib.urlopen(postUrl)
    urlResp = json.loads(urlResp.read())
    logger.info(urlResp)
    return urlResp


'''
    1。去数据库查询是否有toke
            存在 判断失效时间
                未失效 使用
                失效 重新获取，更新toke
            不存在 获取toke 写入并记录 失效时间
'''


def get_access_token():
    modelsToken = accessToken()
    result, status = modelsToken.getAccessToken()
    t = time.time()
    access_token = ''
    if result != []:
        if result['expires_time_stamp'] < int(t):  # 统一使用时间戳 当前时间戳较大，未过期，否则过期重新获取。
            access_token = result['access_token']
            logger.info("get_access_token当前使用的： access_token:{} ,expires_time_stamp:{}".format(access_token, result['expires_time_stamp']))

        else:
            access_token = __real_get_access_token()
            status = modelsToken.updateAccessToken(access_token)
    else:
        access_token = __real_get_access_token()
        status = modelsToken.insertAccessToken(access_token)

    return access_token


def check_access_toke(f):
    @wraps(f)
    def get_self_access_token(*args, **kwargs):
        get_access_token()
        logger.info("获取验证的token")
        return f(*args, **kwargs)

    return get_self_access_token


if __name__ == '__main__':
    print 'hello'
