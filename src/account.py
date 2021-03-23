#!/usr/bin/python

'''
python version: 3.7

该类用于定义单个账户的数据结构
'''

#常量
INC_FLAG = "+"
DEC_FLAG = "-"

class accountClass:
	def __init__(self, _fund, _sharesInfoList):
		#所有数据的外部可见性先暂定为public
		self.fund = _fund	#持有的资金, 尚不明确是整型还是double
		self.stockHolding = [0] * len(_sharesInfoList)	#持有的股票, 列表第i位的数值表示该用户持有第i只股票的数量
		self.stockPriceAndNum = dict()
		self.interest = 0.0	#利息, 尚不明确该属性是否需要，暂不需要，但暂不删除

	def setFund(self, _changeFund, _flag):
		#flag为+则表示增加资金，为-表示减少
		if _flag == INC_FLAG:
			self.fund += _changeFund
		elif _flag == DEC_FLAG and _changeFund <= self.fund:
			self.fund -= _changeFund
		else:
			raise Exception("资金不允许为负, 现有金额-%d 操作金额-%d" % (self.fund, _changeFund))

	def getFund(self):
		return self.fund

	def setInterest(self, _newInterest):
		#暂不实现
		pass

	def getInterest(self):
		#暂不实现
		pass


