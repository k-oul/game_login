#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/16/016 15:29
# @Author  : K_oul
# @File    : to_db.py
# @Software: PyCharm
import datetime
import uuid
from app.db.db import MySQL

my_db = MySQL()

def buyin_to_db(result, token):
    data = {
        'token': token,
        'showId': result.get('showId'),
        'strNick': result.get('strNick'),
        'gameRoomName': str(result.get('gameRoomName').encode()),
        'gameRoomId': result.get('gameRoomId'),
        'buyStack': result.get('buyStack'),
        'uuid': result.get('uuid'),
        'totalBuyin': result.get('totalBuyin'),
        'totalProfit': result.get('totalProfit'),
        'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'status': 0,
    }

    my_db.insert('check_buyin', data)


def history_to_db(history_list, club_id):
    zj_list = [int(i[20]) for i in history_list[1:]]
    zj_max = max(zj_list)
    max_counts = zj_list.count(zj_max)
    zj_min = min(zj_list)
    min_counts = list(zj_list).count(zj_min)
    for temp in history_list[1:]:
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
                'paiju_name': str(temp[1].encode()),
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
            print(data)
            my_db.insert('auto_import', data)
