#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/15/015 15:34
# @Author  : K_oul
# @File    : db.py
# @Software: PyCharm
"""
CREATE TABLE `auto_import` (
  `ID` varchar(40) NOT NULL,
  `room_id` bigint(10) NOT NULL COMMENT '房间ID',   roomId
  `union_account` varchar(20) NOT NULL DEFAULT '' COMMENT '俱乐部账号',
  `paiju_type` varchar(20) NOT NULL DEFAULT '' COMMENT '牌局类型',
  `paiju_name` varchar(40) NOT NULL DEFAULT '' COMMENT '牌局名',
  `jianjuzhe_name` varchar(40) NOT NULL DEFAULT '' COMMENT '建局者昵称',
  `mangzhu` varchar(20) NOT NULL COMMENT '盲注',
  `table` varchar(10) NOT NULL COMMENT '牌桌',
  `shichang` varchar(7) NOT NULL COMMENT '牌局时长',
  `shoushu` int(4) NOT NULL COMMENT '总手数',
  `player_id` bigint(20) NOT NULL COMMENT '玩家ID',
  `player_name` varchar(40) NOT NULL COMMENT '玩家昵称',
  `union_id` bigint(20) NOT NULL COMMENT '俱乐部ID',
  `union_name` varchar(40) NOT NULL COMMENT '俱乐部名称',
  `mairu` int(7) NOT NULL COMMENT '买入',
  `daichu` int(7) NOT NULL COMMENT '带出',
  `baoxian_mairu` int(5) NOT NULL COMMENT '保险买入',
  `baoxian_shouru` int(5) NOT NULL COMMENT '保险收入',
  `baoxian_total` int(7) NOT NULL COMMENT '保险合计',
  `baoxian_club` int(7) NOT NULL COMMENT '俱乐部保险',
  `baoxian` int(7) NOT NULL COMMENT '保险',
  `zhanji` int(7) NOT NULL COMMENT '战绩',
  `over_time` datetime NOT NULL COMMENT '牌局结束时间',
  `update_time` datetime NOT NULL COMMENT '上传时间',
  `encode_paiju_name` varchar(300) NOT NULL DEFAULT '' COMMENT '转码牌局名',
  `status` int(1) unsigned NOT NULL COMMENT '导入结算与否状态',
  `ismvp` int(1) unsigned NOT NULL COMMENT '是否是牌局MVP或最末',
  `count_mvp` int(2) unsigned NOT NULL COMMENT '大鱼或mvp的人数',
  PRIMARY KEY (`ID`,`room_id`),
  UNIQUE KEY `import_depulicate_keys` (`room_id`,`player_id`,`union_id`) USING BTREE
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE `check_buyin` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `gameRoomName` varchar(40) NOT NULL COMMENT '牌局名',
  `gameRoomId` varchar(40) NOT NULL COMMENT '牌局名',
  `showId` varchar(20) NOT NULL COMMENT '玩家ID',
  `strNick` varchar(40) NOT NULL COMMENT '玩家昵称',
  `buyStack` int(7) NOT NULL COMMENT '申请数量',
  `totalBuyin` int(10) NOT NULL COMMENT '总买入',
  `totalProfit` int(10) NOT NULL COMMENT '总盈亏',
  `update_time` datetime NOT NULL COMMENT '申请时间',
  `status` int(1) NOT NULL COMMENT '审核通过或拒绝',
  `token` varchar(255) NOT NULL DEFAULT '' COMMENT 'token',
  `uuid` varchar(20) NOT NULL DEFAULT '' COMMENT 'uuid',
  PRIMARY KEY (`id`),
  UNIQUE KEY `import_depulicate_keys` (`buyStack`,`totalBuyin`,`totalProfit`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4;

"""

import pymysql
from config import *


class MySQL():
    def __init__(self, host=MYSQL_HOST, username=MYSQL_USER, password=MYSQL_PASSWORD, port=MYSQL_PORT,
                 database=MYSQL_DATABASE):
        """
        MySQL初始化
        :param host:
        :param username:
        :param password:
        :param port:
        :param database:
        """
        try:
            self.db = pymysql.connect(host, username, password, database, charset='utf8', port=port)
            self.cursor = self.db.cursor()
        except pymysql.MySQLError as e:
            print('数据库连接错误：', e.args)

    def insert(self, table, data):
        """
        插入数据
        :param table:
        :param data:
        :return:
        """
        keys = '`' + '`,`'.join(data.keys()) + '`'
        values = ', '.join(['%s'] * len(data))
        sql_query = 'insert ignore into %s (%s) values (%s) ' % (table, keys, values)
        try:
            self.cursor.execute(sql_query, tuple(data.values()))
            self.db.commit()
            # print('{} : 入库成功！'.format(table))
        except pymysql.MySQLError as e:
            print('{} : 入库失败！'.format(table), e)
            self.db.rollback()
