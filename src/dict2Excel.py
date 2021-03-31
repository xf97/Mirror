#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
该文件用于将dict输出为excel
待完成
'''

import json
from xlsxwriter import Workbook

#测试，先输出成json文件
FILE_SUFFIX = ".xlsx"

#_year表示当前年份
#_infoDict表示该年份最后一天的收盘价值
def dict2Excel(_year, _infoDict):
	colNameList = [str(i) for i in range(1, 51)]
	colNameList.insert(0, "月份/股票")
	#print(colNameList)
	wb = Workbook(str(_year) + FILE_SUFFIX)
	ws = wb.add_worksheet("本年度各月份各支股票收盘价格")
	_1stRow = 0
	#写入列名
	for header in colNameList:
		col = colNameList.index(header)
		ws.write(_1stRow, col, header)
	#写入后续内容
	row = 1
	for key, value in _infoDict.items():
		#写入月份
		ws.write(row, 0, key)
		#写入数据
		ws.write_row(row, 1, value)
		row += 1
	wb.close()
	print("%d年度数据已保存-%s" % (_year, str(_year) + FILE_SUFFIX))

#单元测试
if __name__ == "__main__":
	a = {"a":[2,3,4,5,52355,5], "b":[23214135,231,531,5]}
	dict2Excel(1,a)


