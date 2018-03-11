import hashlib
from flask import Flask, Blueprint, request, render_template
from flask import jsonify, make_response, abort

app = Flask(__name__)

import os, urllib2, json
from app.utils.MyLogger import MyLogger

logger = MyLogger.getLogger()

from app.weixin.serve.Basic import check_access_toke

cur_abs_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(cur_abs_dir)
templates_folder = os.path.join(os.path.dirname(root_dir), 'templates')

menu_list = Blueprint('MenuController', __name__, url_prefix='/weixin')

class MenuController(object):
    pass

@menu_list.route('/create', methods=['POST'])
@check_access_toke
def MenuCreate():
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + appid + '&secret=' + secret
    response = urllib2.urlopen(url)
    html = response.read()
    tokeninfo = json.loads(html)
    token = tokeninfo['access_token']
    post = ''''' 
     { 
         "button":[ 
         {   
              "type":"click", 
              "name":"开始", 
              "key":"begin" 
          }, 
          { 
               "type":"click", 
               "name":"结束", 
               "key":"end" 
          }, 
          { 
              "type":"click", 
               "name":"游戏", 
               "key":"play"     
           }] 
     }'''
    url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=' + token
    req = urllib2.Request(url, post)
    response = urllib2.urlopen(req)
    return response