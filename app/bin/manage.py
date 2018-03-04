#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from test import app

if __name__ == "__main__":
    app.run()
