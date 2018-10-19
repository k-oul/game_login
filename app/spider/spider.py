#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/8 10:43
# @Author  : K_oul
# @File    : spider.py
# @Software: PyCharm


import schedule
import requests
import json
import time
from time import localtime, strftime, mktime, strptime
from app.spider.excel2list import excel2list
from app.db.to_db import history_to_db
from threading import Thread
from config import USER_AGENT


# 定时获取战绩
class Spider(Thread):
    def __init__(self, token):
        super().__init__()
        self.flag = True
        self.token = token

    def run(self):
        schedule.every(30).seconds.do(get_history_all, self.token)  # 每30秒运行一次
        while self.flag:
            try:
                schedule.run_pending()
                time.sleep(3)
            except Exception as e:
                print('请求错误3秒后重试', e)
                time.sleep(3)


# 获取俱乐部id
def get_club_id(token):
    url = 'http://cms.pokermanager.club/cms-api/club/getClubList'
    headers = {
        'token': token,
        'User-Agent': USER_AGENT,
    }
    try:
        temp = requests.post(url, headers=headers).text
        res = json.loads(temp).get('result')
        if res:
            res = res[0].get('lClubID')  # 默认获取第一个俱乐部id
            print(res)
        else:
            print('token过期请重新登录')
    except Exception as e:
        print('获取club_id失败', e)
    else:
        return str(res)


# 获取俱乐部信息 注册token
def get_club_info(token, club_id):
    url = 'http://cms.pokermanager.club/cms-api/club/clubInfo'
    headers = {
        'token': token,
        'User-Agent': USER_AGENT,
    }
    data = {
        'clubId': club_id,
    }
    requests.post(url, headers=headers, data=data)
    return None


def day_tamp():
    dt = strftime("%Y-%m-%d 00:00:00", localtime(time.time()))
    ts = int(mktime(strptime(dt, "%Y-%m-%d %H:%M:%S"))) * 1000
    return ts


# 获取当天所有战绩
def get_history_all(token):
    url = 'http://cms.pokermanager.club/cms-api/game/exportGameResultList?'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'cms.pokermanager.club',
        'Referer': 'http://cms.pokermanager.club/cms-web/gradeExports.html',
        'User-Agent': USER_AGENT,
    }
    club_id = get_club_id(token)
    startime = day_tamp()
    endtime = startime + 86400000
    params = {
        'clubId': club_id,
        'startTime': str(startime),
        'endTime': endtime,
        'token': token,
        'gameName': '',
        'order': '-1',
        'gameType': '1',
    }
    try:
        r = requests.get(url, headers=headers, params=params)
        if r.status_code == '403':
            print('导出战绩 403')
            return None

        history_list = excel2list(r.content)
    except Exception as e:
        print('获取导出战绩失败', e)
    else:
        if history_list and len(history_list) > 1:
            history_to_db(history_list, club_id)


# def get_history(self):
#     url = 'http://cms.pokermanager.club/cms-api/game/getHistoryGameList'
#     headers = {
#         'token': self.token,
#         'User-Agent': USER_AGENT,
#     }
#     club_id = get_club_id(self.token)
#     startime = day_tamp()
#     endtime = startime + 86400000
#     data = {
#         'clubId': club_id,
#         'startTime': str(startime),
#         'endTime': endtime,
#         'keyword':'',
#         'order': '-1',
#         'gameType': '1', # {普通：1，奥马哈：2，SNG：4，短牌：5，大菠萝：6，全部：7}
#         'pageSize': '10',
#         'pageNumber': '1',
#     }
#     try:
#         temp = requests.post(url,headers=headers, data=data).text
#     except Exception as e:
#         print('获取房间列表失败', e)
#         sleep(5)
#         self.get_history()
#     else:
#         if temp:
#             ls = json.loads(temp).get('result').get('list')
#             for i in ls:
#                 roomId = i.get('roomid')
#                 print(roomId)
#                 get_history_list(self.token, roomId, club_id)
#                 sleep(3)

# 获取牌局战绩
# def get_history_detail(roomId, token):
#     url = 'http://cms.pokermanager.club/cms-api/game/getHistoryGameDetail'
#     headers = {
#         'token': token,
#         'User-Agent': USER_AGENT,
#     }
#     data = {'roomId': roomId}
#     temp = requests.post(url, headers=headers, data=data).text
#     uuid = json.loads(temp).get('result')[0].get('uuid')
#     print(uuid)
#     return uuid
#
# 获取房间列表
# def get_history_list(token, roomId, club_id):
#     url = 'http://cms.pokermanager.club/cms-api/game/exportGame?'
#     headers = {
#         'Host': 'cms.pokermanager.club',
#         'Referer': 'http://cms.pokermanager.club/cms-web/gradeDetail.html?roomid={}'.format(roomId),
#         'User-Agent': USER_AGENT,
#     }
#     params = {
#         'roomId': roomId,
#         'token': token
#     }
#     try:
#         r = requests.get(url, headers=headers, params=params)
#         if r.status_code == '403':
#             print('导出战绩 403 ： ', roomId)
#             return None
#         history_list = excel2list(r.content)
#     except Exception as e:
#         print('获取导出战绩失败', e)
#     else:
#         if history_list and len(history_list) > 1:
#             to_db(history_list, club_id)


if __name__ == '__main__':
    # token = '305c300d06092a864886f70d0101010500034b0030480241008d0dd71584259f6f279b75f1c4ec80168643a8bb5ce0086e38881464c728bda567f3813e5d3683fa60ed873b4ea760de6d4c73c57e06e994610ede95faa2567d0203010001'
    # spider = Spider(token)
    # spider.start()
    pass
