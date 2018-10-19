#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/15/015 18:00
# @Author  : K_oul
# @File    : excel2list.py
# @Software: PyCharm

import xlrd


# 转换excel
def excel2list(file_path):
    if get_data(file_path) is not None:
        book = get_data(file_path)
        # 抓取所有sheet页的名称
        sheet = book.sheet_by_index(0)  # 第一行是表单标题
        nrows = sheet.nrows  # 行号
        # ncols = sheet.ncols  # 列号
        res = []
        for i in range(1, nrows):
            res.append(sheet.row_values(i))
        # print (result)
        return res


# 获取excel数据源
def get_data(file_path):
    try:
        data = xlrd.open_workbook(file_contents=file_path)
        return data
    except Exception as e:
        print('excel表格读取失败：%s' % e)
        return None


if __name__ == '__main__':
    pass
