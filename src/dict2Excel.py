#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
该文件用于将dict输出为excel
待完成
'''

import json

#测试，先输出成json文件
FILE_SUFFIX = ".json"

#_year表示当前年份
#_infoDict表示该年份最后一天的收盘价值
def dict2Excel(_year, _infoDict):
	with open(str(_year) + FILE_SUFFIX, "w") as f:
			f.write(json.dumps(_infoDict, indent = 1))


#单元测试
if __name__ == "__main__":
	a = {1:"2", 2:"3"}
	dict2Excel(1,a)


