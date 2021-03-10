#!/usr/bin/python

'''
python version: 3.7

该类用于定义单个账户的数据结构
'''

class accountClass:
	def __init__(self, _sharesNum):
		#所有数据的外部可见性先暂定为public
		self.fund = 0	#持有的资金, 尚不明确是整型还是double
		self.stockHolding = [0] * _sharesNum	#持有的股票, 列表第i位的数值表示该用户持有第i只股票的数量
		self.interest = 0.0	#利息, 尚不明确该属性是否需要


