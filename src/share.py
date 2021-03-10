#!/usr/bin/python

'''
python version: 3.7

该类用于定义单只股票的数据结构
'''

class shareClass:
	#_nOfShare means the number of the share
	#_prob指的是账户想购买这只股票的概率
	def __init__(self, _price, _nOfShare, _probList, _upperPirce, _lowerPrice):
		self.price = _price
		self.number = _nOfShare
		self.probList = _probList
		self.bidRange = [_lowerPrice, _upperPirce]