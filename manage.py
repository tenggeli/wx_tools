#!/usr/bin/env python
# -*- coding:utf8 -*-
import os

from flask_script import Manager
from app.bin.main import app

manager = Manager(app)


@manager.command
def deploy():
    print ('！！！！！开始执行！！！！！')
if __name__ == '__main__':
    manager.run()
