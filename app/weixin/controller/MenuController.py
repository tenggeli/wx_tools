# -*- coding: utf-8 -*-


import hashlib
from flask import Flask, Blueprint, request, render_template
from flask import jsonify, make_response, abort

app = Flask(__name__)

import os, urllib2, json
from app.utils.MyLogger import MyLogger

logger = MyLogger.getLogger()

from app.weixin.serve.Basic import get_access_token

cur_abs_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(cur_abs_dir)
templates_folder = os.path.join(os.path.dirname(root_dir), 'templates')

menu_list = Blueprint('MenuController', __name__, url_prefix='/weixin')

class MenuController(object):
    pass

@menu_list.route('/menu_create', methods=['GET'])
def MenuCreate():
    token = get_access_token()
    print (token)
    post = ''''' 
     { 
         "button":[ 
         {   
              "type":"click", 
              "name":"菜单1", 
              "key":"begin" 
          }, 
          { 
               "type":"click", 
               "name":"菜单2", 
               "key":"end" 
          }, 
          { 
              "type":"click", 
               "name":"菜单3", 
               "key":"play"     
           }] 
     }'''
    url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=' + token
    req = urllib2.Request(url, post)
    response = urllib2.urlopen(req)
    return response