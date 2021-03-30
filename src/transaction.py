#!/usr/bin/python

'''
python version: 3.7

该类用于定义交易数据(需要被存储的部分)的数据结构
'''

import math

class transactionClass:
	def __init__(self, _shareNum):
		#因交易数据尚不明确, 此类暂不明确
		#存储每只股当天和前一天的交易量
		#print(_shareNum, type(_shareNum))
		self.yesterdayTransactionList = [0] * _shareNum
		self.todayTransactionList = [0] * _shareNum
		self.totalTransactionNum = [0] * _shareNum #记录每只股票的总交易量
		self.shareNum = _shareNum

	#新的一天来到
	def newDayComes(self):
		#深度复制
		self.yesterdayTransactionList = self.todayTransactionList[:]	
		self.todayTransactionList = [0] * self.shareNum

	#设置新的一笔交易量，以加等于的形式
	def newTransactionComes(self, _shareIndex, _transNum):
		self.todayTransactionList[_shareIndex] += _transNum
		self.totalTransactionNum[_shareIndex] += _transNum 

	#获得昨天的一只股票的交易量
	def getYesterdayTransNum(self, _shareIndex):
		return self.yesterdayTransactionList[_shareIndex]

	#获得今天一只股票的交易量
	def getTodayTransNum(self, _shareIndex):
		return self.todayTransactionList[_shareIndex]

	#获得今天一只股票的交易平均值
	def getTodayAveTransNum(self):
		result = sum(self.todayTransactionList)/ len(self.todayTransactionList)
		#如果今日无交易，就用昨日的数据代替
		if math.isclose(result, 0):
			result = self.getYesterdayAveTransNum()
		return result

	#获得昨日股票的平均交易数量
	def getYesterdayAveTransNum(self):
		return sum(self.yesterdayTransactionList) / len(self.yesterdayTransactionList)

	#获得每只股票总交易量
	def getTotalTransactionNum(self, _index = -1):
		if _index == -1:
			#返回所有股票的交易列表
			return self.totalTransactionNum
		else:
			return list(self.totalTransactionNum[_index])

	#清空数据
	def clear(self):
		self.yesterdayTransactionList = [0] * self.shareNum
		self.todayTransactionList = [0] * self.shareNum
		self.totalTransactionNum = [0] * self.shareNum #记录每只股票的总交易量		

#单元测试
if __name__ == "__main__":
	tc = transactionClass(50)
	tc.newTransactionComes(1, 50000)
	tc.newTransactionComes(10, 2000000)
	tc.newTransactionComes(12, 22100000)	
	tc.newTransactionComes(29, 213100000)	
	tc.newTransactionComes(23, 2100000)
	print(tc.getYesterdayAveTransNum())	
	tc.newDayComes()
	print(tc.getYesterdayAveTransNum())			