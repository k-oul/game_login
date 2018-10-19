#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/30/030 9:37
# @Author  : K_oul
# @File    : login.py
# @Software: PyCharm

import json
import requests
from Crypto.Util.py3compat import bord
from hashlib import md5
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from base64 import b64encode
from binascii import unhexlify
from config import USER_AGENT


headers = {
        'Host': 'cms.pokermanager.club',
        'Origin': 'http://cms.pokermanager.club',
        'Referer': 'http://cms.pokermanager.club/cms-web/cmsLogin.html',
        'User-Agent': USER_AGENT
    }

def get_token():
    url = 'http://cms.pokermanager.club/cms-api/token/generateCaptchaToken'
    html = requests.get(url,headers=headers).text
    token = json.loads(html).get('result')
    print(token)
    return token


def get_captcha(token):
    c_url = 'http://cms.pokermanager.club/cms-api/captcha'
    html = requests.post(c_url, data={'token': token}).text
    res = json.loads(html).get('result')
    # print(res)
    return res


def pwd_md5(pwd):
    hash = md5()
    hash.update(pwd.encode('utf-8'))
    return "".join("%x" % bord(x) for x in hash.digest())


def get_data(token, user, pwd):
    msg = '{},{}'.format(user, pwd_md5(pwd))
    keyDER = unhexlify(token)
    keyPub = RSA.importKey(keyDER)
    cipher = PKCS1_v1_5.new(keyPub)
    cipher_text = cipher.encrypt(msg.encode())
    emsg = b64encode(cipher_text).decode()
    # print(emsg)
    return emsg


def login_in(token, user, pwd, code):
    # 模拟登录
    url = 'http://cms.pokermanager.club/cms-api/login'
    data = {
        'token': token,
        'data': get_data(token, user, pwd),
        'safeCode': code,
        'locale': 'zh',
    }
    html = requests.post(url, headers=headers, data=data)
    print(html.status_code, html.text)
    return html.text

if __name__ == '__main__':
    pass
