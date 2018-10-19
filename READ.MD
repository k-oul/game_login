
#### python 3.6.5

```
  pip install -r requirements.txt
```

#### 审核数据表单
```
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
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

```


#### API
```
/accept  |  /deny
args : uuid , roomId, token
```
