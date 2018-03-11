#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import os
from flask import Flask, render_template, Blueprint
from flask import request

cur_abs_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(cur_abs_dir)
code_dir = os.path.dirname(root_dir)  # /Users/xiaoqi/www/MyHtml/wx_tools/app
sys.path.insert(0, code_dir)  # /Users/xiaoqi/www/MyHtml/wx_tools
from app.utils.MyLogger import MyLogger

logger = MyLogger.getLogger()

from app.weixin.controller.IngressController import ingress
from app.weixin.controller.MenuController import menu_list
# from app.weixin.serve.Basic import basic

# lc = LoginController()

# 设置系统静态文件和模版文件
static_floder = os.path.join(root_dir, 'static')
template_folder = os.path.join(root_dir, 'templates')

app = Flask(__name__, static_folder=static_floder,
            template_folder=template_folder)

# app.register_blueprint(handle)
app.register_blueprint(ingress, url_prefix='/weixin')
app.register_blueprint(menu_list, url_prefix='/weixin')
# app.register_blueprint(basic)


@app.route('/')
def index():
    return render_template('index/index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=443)
