#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
该文件用于为给定的列表进行有指定上下限的归一化
'''

__author__ = "__xiaofeng__"

from random import shuffle	#用于随机打乱数组


#_list是给定的、需要被归一化的数组
#_highLimit是归一化的上限
#_lowLimit是归一化的下限
def normalization(_list, _highLimit, _lowLimit):
	#归一化公式
	'''
	result = ((x - min) / (max - min)) * _highLimit + ((x - max) / (min - max)) * _lowLimit 
	'''
	maxValue = max(_list)
	minValue = min(_list)
	resultList = [0.0] * len(_list)
	for index, value in enumerate(_list):
		try:
			resultList[index] = (((value - minValue) / (maxValue - minValue)) * _highLimit + ((value - maxValue) / (minValue - maxValue)) * _lowLimit)
			#resultList[index] -= 0.5
		except ZeroDivisionError:
			#对除0错误进行处理
			resultList[index] = 1.0
	return resultList

#单元测试
if __name__ == "__main__":
	result = list(range(10))
	shuffle(result)
	print(result)
	result = normalization(result, 1.1 - 1e-5, 0.9 + 1e-5)
	print(result)



