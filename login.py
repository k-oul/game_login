#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/30/030 9:37
# @Author  : K_oul
# @File    : login.py
# @Software: PyCharm

import json

import re

import time
from Crypto.Util.py3compat import bord
from requests import session
import requests
from hashlib import md5

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from base64 import b64decode,b64encode

from binascii import  unhexlify



class Login():
    def __init__(self):
        self.headers = {
            'token': '',
            'Host': 'cms.pokermanager.club',
            'Origin': 'http://cms.pokermanager.club',
            'Pragma': 'no-cache',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://cms.pokermanager.club/cms-web/cmsLogin.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        self.req = requests.session()
        self.username = '56035705'
        self.password = '123456789'

        self.token = self.get_token()
        self.data = self.get_data()

    def pwd_md5(self):
        hash = md5()
        hash.update(self.password.encode('utf-8'))
        return "".join("%x" % bord(x) for x in hash.digest())

    def get_data(self):
        msg = '{},{}'.format(self.username, self.pwd_md5())
        keyDER = unhexlify(self.token)
        keyPub = RSA.importKey(keyDER)
        cipher = Cipher_PKCS1_v1_5.new(keyPub)
        cipher_text = cipher.encrypt(msg.encode())
        emsg = b64encode(cipher_text).decode()
        print(emsg)
        return emsg

    def get_token(self):
        self.req.headers.update(self.headers)
        t_url = 'http://cms.pokermanager.club/cms-api/token/generateCaptchaToken'
        html = self.req.get(t_url).text
        token = json.loads(html).get('result')
        print(token)
        return token

    def get_captcha(self):
        c_url = 'http://cms.pokermanager.club/cms-api/captcha'
        html = self.req.post(c_url, data={'token': self.token}).text
        res = 'data:image/jpg;base64,' + json.loads(html).get('result')
        print(res)

    def login(self):
        url = 'http://cms.pokermanager.club/cms-api/login'
        data = {
            'token': self.token,
            'data': self.data,
            'safeCode': input('please input safeCode : '),
            'locale': 'zh'
        }
        html = self.req.post(url, data=data)
        self.headers.update({'token': self.token})
        print(html.status_code, html.text)

    def get_history(self):
        url = 'http://cms.pokermanager.club/cms-api/game/getHistoryGameList'
        headers = {
            'token': self.token,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        }
        data = {
            'clubId': '889999',
            'startTime': '1539014400000',
            'endTime': '1539100800000',
            'keyword': '',
            'order': '-1',
            'gameType': '1',  # {普通：1，奥马哈：2，SNG：4，短牌：5，大菠萝：6，全部：7}
            'pageSize': '10',
            # 'pageNumber': '1',
        }
        r = requests.post(url, headers=headers, data=data).text
        total = json.loads(r).get('result').get('total')
        data.update({'pageSize': total})
        r = requests.post(url, headers=headers, data=data).text
        print(r)





if __name__ == '__main__':
    # main()

    login = Login()
    login.get_captcha()
    login.login()
    time.sleep(2)
    login.get_history()

