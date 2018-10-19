#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/19/019 9:51
# @Author  : K_oul
# @File    : routes.py
# @Software: PyCharm

import base64
import json

from app.forms import LoginForm
from app.spider.check_buyin import CheckBuyin, accept_buyin, deny_buyin
from app.spider.login import get_token, get_captcha, login_in
from app.spider.spider import Spider
from app import app
from flask import render_template, flash, redirect, session, make_response, request, jsonify


# 获取验证码
@app.route('/code', methods=['GET', 'POST'])
def code():
    token = get_token()
    code_url = get_captcha(token)
    code_img = base64.b64decode(code_url)
    response = make_response(code_img)
    response.headers['Content-Type'] = 'image/git'
    session['token'] = token
    return response


# 通过api
@app.route('/accept')
def accept():
    uuid = request.args.get('uuid')
    roomId = request.args.get('roomId')
    token = request.args.get('token')
    r = accept_buyin(uuid, roomId, token)
    return jsonify(r)


# 拒绝api
@app.route('/deny')
def deny():
    uuid = request.args.get('uuid')
    roomId = request.args.get('roomId')
    token = request.args.get('token')
    r = deny_buyin(uuid, roomId, token)
    return jsonify(r)


# 登录验证
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        verify_code = form.verify_code.data
        try:
            token = session.get('token')
            print(token)
            res = login_in(token=token, user=username, pwd=password, code=verify_code)
            iErrCode = json.loads(res).get('iErrCode')
            if iErrCode == 0:
                flash('登录成功, 爬虫已启动！！！')
                spider = Spider(token)
                spider.start()
                check = CheckBuyin(token)
                check.start()
                return redirect('/')
            elif iErrCode == 1103:
                flash('验证码错误')
                return redirect('/')
            else:
                flash('登录失败，请检查账号密码')
                return redirect('/')
        except Exception as e:
            print('Error', e)
            return redirect('/')
    return render_template('login.html', form=form)
