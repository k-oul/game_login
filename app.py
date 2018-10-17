#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/12/012 18:19
# @Author  : K_oul
# @File    : app.py
# @Software: PyCharm
import json
import base64
from asyncio import sleep

from flask import Flask, render_template, request, flash, redirect, url_for, session, make_response, jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

from check import buyin_run
from login import get_token, get_captcha, login_in

from spider import history_run

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    verify_code = StringField('验证码', validators=[DataRequired()])
    submit = SubmitField('登录')

@app.route('/buyin')
def buyin():
    token = session.get('token')
    buyin_run(token)



@app.route('/code', methods=['GET', 'POST'])
def code():

    token = get_token()
    code_url = get_captcha(token)
    code = base64.b64decode(code_url)
    response = make_response(code)
    response.headers['Content-Type'] = 'image/git'
    session['token'] = token
    return response



@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        verify_code = form.verify_code.data
        try:
            token =session.get('token')
            print(token)
            res = login_in(token=token ,user=username,pwd=password,code=verify_code)
            iErrCode = json.loads(res).get('iErrCode')
            if iErrCode == 0:
                flash('登录成功, 爬虫已启动！！！')
                # history_run(token)
                # buyin_run(token)

            elif iErrCode == 1103:
                flash('验证码错误')
            else:
                flash('登录失败，请检查账号密码')
        except Exception as e:
            print('Error', e)
        return redirect('/')
    return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
