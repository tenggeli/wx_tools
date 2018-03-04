#!/usr/bin/env python
# -*- coding:utf8 -*-

from flask_script import Manager
from main import app

manager = Manager(app)

if __name__ == '__main__':
    manager.run()
