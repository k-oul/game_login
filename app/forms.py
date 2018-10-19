#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/19/019 10:01
# @Author  : K_oul
# @File    : forms.py
# @Software: PyCharm

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    verify_code = StringField('验证码', validators=[DataRequired()])
    submit = SubmitField('登录')