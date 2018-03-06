# -*- coding: utf-8 -*-
#  filename: basic.py

import os, time
from flask import Flask, Blueprint, request
from flask import jsonify, abort, render_template
from functools import wraps

app = Flask(__name__)


from app.utils.MyLogger import MyLogger

logger = MyLogger.getLogger()

# print(logger)

#
# import urllib
# import time
# import json
# from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
# import MySQLdb


cur_abs_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(cur_abs_dir)
templates_folder = os.path.join(os.path.dirname(root_dir), 'templates')

basic = Blueprint('basic', __name__)


# engine = create_engine("mysql+mysqldb://root:root@127.0.0.1:3306/test", max_overflow=5)

class Basic:
    pass

    # def __init__(self):
    #     self.__accessToken = ''
    #     self.__leftTime = 0


def __real_get_access_token(self):
    appId = "wxe2b38dabbb686f21"
    appSecret = "8e511b955bab52120e2f821684ea7859"

    postUrl = (
        "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (appId, appSecret))

    urlResp = urllib.urlopen(postUrl)
    urlResp = json.loads(urlResp.read())
    self.__accessToken = urlResp['access_token']
    self.__leftTime = urlResp['expires_in']


'''
    1。去数据库查询是否有toke
            存在 判断失效时间
                未失效 使用
                失效 重新获取，更新toke
            不存在 获取toke 写入并记录 失效时间
'''


def get_access_token():

    print ('xxxxx')
    # if self.__leftTime < 10:
    #     self.__real_get_access_token()
    #     return self.__accessToken


def run(self):
    while (True):
        if self.__leftTime > 10:
            time.sleep(2)
            self.__leftTime -= 2
        else:
            self.__real_get_access_token()


def check_access_toke(f):
    @wraps(f)
    def get_self_access_token(*args, **kwargs):
        get_access_token()
        return f(*args, **kwargs)

    return get_self_access_token


if __name__ == '__main__':
    print 'hello'
