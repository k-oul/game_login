#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/17/017 9:35
# @Author  : K_oul
# @File    : check_buyin.py
# @Software: PyCharm

import json
import requests
from time import sleep
from threading import Thread
from app.db.to_db import buyin_to_db
from app.spider.spider import get_club_id, get_club_info
from config import USER_AGENT


# 获取带入审核数据
class CheckBuyin(Thread):
    def __init__(self, token):
        super().__init__()
        self.buyin_flag = True
        self.token = token

    def get_buyin(self):
        url = 'http://cms.pokermanager.club/cms-api/game/getBuyinList'
        headers = {
            'token': self.token,
            'User-Agent': USER_AGENT,
        }
        try:
            r = requests.post(url, headers=headers).text
            if r:
                temp = json.loads(r)
                if temp:
                    print(temp)
                    res = temp.get('result')
                    if res is not None:
                        for i in res:
                            buyin_to_db(i, self.token)  # 存入数据库
                return None

        except Exception as e:
            print('获取当前带入审核个数失败', e.args)
            print('5秒后重试')
            sleep(5)
            self.get_buyin()

    def run(self):
        club_id = get_club_id(self.token)
        get_club_info(self.token, club_id)
        while self.buyin_flag:
            try:
                self.get_buyin()
                sleep(3)
            except Exception as e:
                print('请求错误3秒后重试', e.args)
                sleep(3)
                continue


# 通过
def accept_buyin(uuid, roomId, token):
    """
    数据库表check_buying获取
    :param uuid:
    :param roomId:
    :param token:
    :return:
    """

    url = 'http://cms.pokermanager.club/cms-api/game/acceptBuyin'
    headers = {
        'token': token,
        'User-Agent': USER_AGENT,
    }
    data = {
        'userUuid': uuid,
        'roomId': roomId,
    }
    r = requests.post(url, headers=headers, data=data)
    return r.text


# 拒绝
def deny_buyin(uuid, roomId, token):
    url = 'http://cms.pokermanager.club/cms-api/game/denyBuyin'
    headers = {
        'token': token,
        'User-Agent': USER_AGENT,
    }
    data = {
        'userUuid': uuid,
        'roomId': roomId,
    }
    r = requests.post(url, headers=headers, data=data)
    print(r.text)


if __name__ == '__main__':
    pass
