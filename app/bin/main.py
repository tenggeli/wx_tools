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

from app.weixin.handle import handle
from app.weixin.basic import check_access_toke
from app.weixin.basic import basic

# lc = LoginController()

# 设置系统静态文件和模版文件
static_floder = os.path.join(root_dir, 'static')
template_folder = os.path.join(root_dir, 'templates')

# app = Flask(__name__, static_folder=static_floder, template_folder=template_folder)
app = Flask(__name__)

# app.register_blueprint(handle)
app.register_blueprint(handle, url_prefix='/weixin')
app.register_blueprint(basic)


# 需要在main外面，uwsgi调用不会执行main
# application = app.wsgifunc()

@app.route('/')
# @basic
def index():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=443)
