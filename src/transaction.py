#!/usr/bin/python

'''
python version: 3.7

该类用于定义交易数据(需要被存储的部分)的数据结构
'''

class transactionClass:
	def __init__(self, _shareNum):
		#因交易数据尚不明确, 此类暂不明确
		#存储每只股当天和前一天的交易量
		self.yesterdayTransactionList = [0] * _shareNum
		self.todayTransactionList = [0] * _shareNum
		self.shareNum = _shareNum

	#新的一天来到
	def newDayComes(self):
		#深度复制
		self.yesterdayTransactionList = self.todayTransactionList[:]	
		self.todayTransactionList = [0] * self.shareNum

	#设置新的一笔交易量，以加等于的形式
	def newTransactionComes(self, _shareIndex, _transNum):
		self.todayTransactionList[_shareIndex] += _transNum

	#获得昨天的一只股票的交易量
	def getYesterdayTransNum(self, _shareIndex):
		return self.yesterdayTransactionList[_shareIndex]

	#获得今天一只股票的交易量
	def getTodayTransNum(self, _shareIndex):
		return self.todayTransactionList[_shareIndex]

	#获得昨日股票的平均交易数量
	def getYesterdayAveTransNum(self):
		return sum(self.yesterdayTransactionList) / len(self.yesterdayTransactionList)


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