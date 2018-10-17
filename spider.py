#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/8 10:43
# @Author  : K_oul
# @File    : spider.py
# @Software: PyCharm

import datetime
import requests
import json
import uuid

from time import time, localtime, strftime, mktime, strptime,sleep
import asyncio
from excel2list import excel2list
from db import MySQL

my_sql = MySQL()
flag = 1

# token = '305c300d06092a864886f70d0101010500034b003048024100bb565206ce083e7c782008138ab0239361a9bc9be857486e07b7a59ebd72ff9acb04a2fcbda5c94bc1119207eba7395c0df18968e4d7746106583c45202b0e450203010001'
def get_history(token):
    url = 'http://cms.pokermanager.club/cms-api/game/getHistoryGameList'
    headers = {
        'token': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    }
    club_id = get_club_id(token)
    startime = day_tamp()
    endtime = startime + 86400000
    data = {
        'clubId': club_id,
        'startTime': str(startime),
        'endTime': endtime,
        'keyword':'',
        'order': '-1',
        'gameType': '1', # {普通：1，奥马哈：2，SNG：4，短牌：5，大菠萝：6，全部：7}
        'pageSize': '10',
        'pageNumber': '1',
    }
    try:
        temp = requests.post(url,headers=headers, data=data).text
    except Exception as e:
        print('获取房间列表失败', e)
        sleep(10)
        get_history(token)
    else:
        if temp:
            ls = json.loads(temp).get('result').get('list')
            for i in ls:
                roomId = i.get('roomid')
                print(roomId)
                get_history_list(token, roomId, club_id)
                sleep(3)


# def get_history_detail(roomId, token):
#     url = 'http://cms.pokermanager.club/cms-api/game/getHistoryGameDetail'
#     headers = {
#         'token': token,
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
#     }
#     data = {'roomId': roomId}
#     temp = requests.post(url, headers=headers, data=data).text
#     uuid = json.loads(temp).get('result')[0].get('uuid')
#     print(uuid)
#     return uuid

def get_club_id(token):
    url = 'http://cms.pokermanager.club/cms-api/club/getClubList'
    headers = {
        'Host': 'cms.pokermanager.club',
        'token': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    }
    try:
        temp = requests.post(url, headers=headers).text
        res = json.loads(temp).get('result')
        if res:
            res = res[0].get('lClubID')
            print(res)

        else:
            print('token过期请重新登录')
    except Exception as e:
        print('获取club_id失败', e)
    else:
        return str(res)

def day_tamp():
    dt = strftime("%Y-%m-%d 00:00:00", localtime(time()))
    ts = int(mktime(strptime(dt, "%Y-%m-%d %H:%M:%S"))) * 1000
    return ts


def get_history_list(token, roomId, club_id):
    url = 'http://cms.pokermanager.club/cms-api/game/exportGame?'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'cms.pokermanager.club',
        'Referer': 'http://cms.pokermanager.club/cms-web/gradeDetail.html?roomid={}'.format(roomId),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    }
    params = {
        'roomId': roomId,
        'token': token
    }
    try:
        r = requests.get(url, headers=headers, params=params)
        if r.status_code == '403':
            print('导出战绩 403 ： ', roomId)
            return None

        history_list = excel2list(r.content)
    except Exception as e:
        print('获取导出战绩失败', e)
    else:
        if history_list and len(history_list) > 1:
            to_db(history_list, club_id)


def to_db(history_list, club_id):
    zj_list = [int(i[20]) for i in  history_list[1:]]
    zj_max = max(zj_list)
    max_counts = zj_list.count(zj_max)
    zj_min = min(zj_list)
    min_counts = list(zj_list).count(zj_min)
    for  temp in history_list[1:]:
        if temp[11] == club_id:
            ismvp = 0
            count_mvp = 0
            if int(temp[20]) == zj_max:
                ismvp = 1
                count_mvp = max_counts
            elif int(temp[20]) == zj_min:
                ismvp = 2
                count_mvp = min_counts

            data = {
                'ID': str(uuid.uuid1()),
                'room_id': temp[2],
                'union_account': temp[12],
                'paiju_type': temp[0],
                'paiju_name': temp[1].encode(),
                'jianjuzhe_name': temp[3],
                'mangzhu': temp[4],
                'table': temp[6],
                'shichang': temp[7],
                'shoushu': temp[8],
                'player_id': temp[9],
                'player_name': temp[10],
                'union_id': temp[11],
                'union_name': temp[12],
                'mairu': temp[13],
                'daichu': temp[14],
                'baoxian_mairu': temp[15],
                'baoxian_shouru': temp[16],
                'baoxian_total': temp[17],
                'baoxian_club': temp[18],
                'baoxian': temp[19],
                'zhanji': temp[20],
                'over_time': temp[21],
                'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'encode_paiju_name': str(temp[1].encode()),
                'status': 0,
                'ismvp': ismvp,
                'count_mvp': count_mvp,
            }
            my_sql.insert('auto_import', data)
            print('********************数据库操作成功********************')

def get_history_all(token):
    url = 'http://cms.pokermanager.club/cms-api/game/exportGameResultList?'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'cms.pokermanager.club',
        'Referer': 'http://cms.pokermanager.club/cms-web/gradeExports.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    }
    club_id = get_club_id(token)
    startime = day_tamp()
    endtime = startime + 86400000
    params = {
        'clubId': club_id,
        'startTime': str(startime),
        'endTime': endtime,
        'token': token,
        'gameName':'',
        'order': '-1',
        'gameType': '1',
    }
    try:
        r = requests.get(url, headers=headers, params=params)
        if r.status_code == '403':
            print('导出战绩 403' )
            return None

        history_list = excel2list(r.content)
    except Exception as e:
        print('获取导出战绩失败', e)
    else:
        if history_list and len(history_list) > 1:
            to_db(history_list, club_id)


def history_run(token):
    while flag:
        try:
            get_history(token)
            sleep(30)
        except Exception as e:
            print('请求错误3秒后重试',e)
            sleep(3)
            continue







if __name__ == '__main__':
    get_history_all(token)
    # get_history(token)
    # history_run(token)
    # buyin_run(token)
    # get_club_id(token)
    # get_history_list(token)