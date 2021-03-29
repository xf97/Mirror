#!/usr/bin/python

'''
python version: 3.7

该类用于定义单只股票的数据结构
'''
__author__ = "xiaofeng"
ENABLE_STOP_FLAG = 1
UNABLE_STOP_FLAG = 0

from constant import *
import math

class shareClass:
	#_nOfShare means the number of the share
	#_prob指的是账户想购买这只股票的概率
	def __init__(self, _price, _nOfShare, _probList, _id):
		self.price = _price 	#当前价格
		self.number = _nOfShare	#股票数量
		self.probList = _probList	#想买概率
		#这两个值设定后当天就不会再更改, 直到第二天重设
		self.priceUpperLimit = self.getUpperLimit()	#设定当天上限
		self.priceLowerLimit = self.getLowerLimit()	#设定当天下限 
		self.bidLowLimit = self.priceLowerLimit 	#出价下限
		self.bidHighLimit = self.priceUpperLimit	#出价上限
		self.stopFlag = False	#可否交易标志
		self.upStopFlag = False	#涨停标志
		self.downStopFlag = False #跌停标志
		self.shareId = _id	#股票ID

	#打印对象使用
	def __str__(self):
		msg = "股票ID " + str(self.shareId) + "\n"
		msg += ("当天涨跌上下限 " + str(self.priceUpperLimit) + " " + str(self.priceLowerLimit) + "\n")
		msg += ("当天出价上下限 " + str(self.bidHighLimit) + " " + str(self.bidLowLimit) + "\n")
		msg += ("价格 " + str(self.price) + "\n")
		msg += ("股票数量 " + str(self.number) + "\n")
		msg += ("允许交易标志 " + str(self.stopFlag) + "\n")
		msg += ("想买概率 " + str(len(self.probList)) + "\n")
		msg += "\n"
		return msg

	def getUpperLimit(self):
		return self.price * UPPER_LIMIT

	def getLowerLimit(self):
		return self.price * LOWER_LIMIT

	#新的一天到来，更新当天涨跌和出价上下限
	def setLowerAndUpperLimit(self):
		self.priceUpperLimit = self.price * UPPER_LIMIT
		self.priceLowerLimit = self.price * LOWER_LIMIT
		self.bidLowLimit = self.priceLowerLimit
		self.bidHighLimit = self.priceUpperLimit

	#_flag用于忽视涨跌停规则，用于初始化股票时
	def setPrice(self, _newPrice, _flag):
		if _newPrice > self.bidHighLimit or _newPrice < self.bidLowLimit:
			raise Exception("无效的价格 %d" % _newPrice)
			return False
		elif self.getStopFlag() == True:
			print("本日针对第%d只股票的交易价格触发涨跌停条件，今日不再对该股票进行交易" % (self.shareId))
			return False
		else:
			#否则是有效价格
			#价格上升，更新上下限
			#确认价格
			tempLowLimit = _newPrice * LOWER_LIMIT
			if tempLowLimit < self.priceLowerLimit:
				tempLowLimit = self.priceLowerLimit
			tempHighLimit = _newPrice * UPPER_LIMIT
			if tempHighLimit > self.priceUpperLimit:
				tempHighLimit = self.priceUpperLimit
			self.bidLowLimit = tempLowLimit
			self.bidHighLimit = tempHighLimit
			self.price = _newPrice
			#判断是否涨停或跌停
			#注意浮点数比较相等
			if _flag == UNABLE_STOP_FLAG:
				#不启用涨跌停规则
				return True
			elif _flag == ENABLE_STOP_FLAG:
				if math.isclose(self.price, self.bidHighLimit):
					#涨停
					self.upStopFlag = True
				elif math.isclose(self.price, self.bidLowLimit):
					#跌停
					self.downStopFlag = True
				return True

	def getPrice(self):
		return self.price

	def getNumberOfShare(self):
		return self.number

	#_year指的是当前是第几年
	def getPurchaseProb(self, _year):
		if _year < 0 or _year >= len(self.probList):
			raise Exception("错误的年份 %d" % _year)
		else:
			#否则应该返回对应年份的想买概率
			return self.probList[_year]

	def getBidRange(self):
		#返回出价范围
		return (self.bidLowLimit, self.bidHighLimit)

	def getStopFlag(self):
		return self.upStopFlag or self.downStopFlag

	def resetStopFlag(self):
		self.upStopFlag = False
		self.downStopFlag = False

	def getShareId(self):
		return self.shareId

	def dailyInit(self, _newPrice = 0.0):
		#更新价格，更新出价范围，更新交易准许符
		if not math.isclose(_newPrice, 0.0):
			self.setPrice(_newPrice)
		self.resetStopFlag()
		self.setLowerAndUpperLimit()

#单元测试
if __name__ == "__main__":
	probList = [1] * 20
	aShare = shareClass(10, 10000, probList, 1)
	print(aShare.getPrice())
	print(aShare.getBidRange())
	print(aShare.getShareId())
	print(aShare.getStopFlag())
	print(aShare.getPurchaseProb(19))
	print(aShare.setPrice(11))
	print(aShare.getPrice())
	print(aShare.getBidRange())
	print(aShare.getShareId())
	print(aShare.getStopFlag())
	print(aShare.dailyInit())
	print(aShare.setPrice(10.5))