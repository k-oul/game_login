#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/17/017 9:35
# @Author  : K_oul
# @File    : check.py
# @Software: PyCharm
import json
from time import sleep

import requests

buyin_flag = 1
token = '305c300d06092a864886f70d0101010500034b003048024100aeecab898087ec177a43046e8bb9f5f400f83878fcdd75593cb192f6f63997cb8a9a98f70e3793fcf7450a17f5b00c3182350217b1a551f32ca036b6b658d69f0203010001'
def get_buyin(token):
    url = 'http://cms.pokermanager.club/cms-api/game/getBuyinList'
    headers = {
        'Cookie': 'userLanguage=zh; aliyungf_tc=AQAAAJI9/XoL9gwAYkM5cXkg7r8HzkUP',
        'Host': 'cms.pokermanager.club',
        'Referer': 'http://cms.pokermanager.club/cms-web/buyinConfirmation.html',
        'token': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    }
    try:
        r = requests.post(url,headers=headers).text
        if r:
            result = json.loads(r)
            print(result)
            return result
    except Exception as e:
        print('获取当前带入审核个数失败', e)
        print('5秒后重试')
        sleep(5)
        get_buyin(token)


def buyin_run(token):
    while buyin_flag:
        try:
            get_buyin(token)
            sleep(3)
        except Exception as e:
            print('请求错误3秒后重试',e)
            sleep(3)
            continue

if __name__ == '__main__':
    buyin_run(token)