#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/19/019 9:52
# @Author  : K_oul
# @File    : __init__.py.py
# @Software: PyCharm

from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

from app import routes