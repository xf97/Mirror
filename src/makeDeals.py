#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
该文件用于编写用于交易的函数
从而将该函数从主文件中抽取出来
'''

__author__ = "xiaofeng"

#常量
#偏移值，用于包含随机数上限
STAND_BIAS = 1e-8
#标准差，要改成动态值
SIGMA = 0.5
#最小整笔交易数
LEAST_NUM = 100
#正态分布数组长度
NORMAL_LIST_LENGTH = 100

#导入文件
import random
from scipy import stats as st
import math
import numpy
#账户数据结构，股票数据结构，每日交易信息保存数据结构，年报数据结构，常量
from account import accountClass as ac
from share import shareClass as sc
from transaction import transactionClass as tc
from annualReport import annualReportClass as arc
from constant import * 
import time

'''
_user1是买方，_user2是卖方
买卖_shareIndex股票
交易的价格要在允许区间内
成交后价格需要记录和变动
成交的数据要记录
'''

def getNormalListBias(_low, _high, _loc, _bias, _coolingValue):
	#_bias表示的是出价均值的偏移幅度，值在[0.9-1.1]之间
	#_coolingValue用来抑制连续涨跌造成的价格变动过大
	#该函数生成一个符合正态分布的，值在[_low, _high]之间的序列
	'''
	if not math.isclose(_coolingValue, 1.0):
		print("原始损益-%.2f" % _bias, end = " ")
	'''
	_bias = 1 + (_bias - 1) * _coolingValue
	'''
	if not math.isclose(_coolingValue, 1.0):
		print("实际损益-%.2f, 冷却因子-%.2f" % (_bias, _coolingValue))
	'''
	meanValue = _loc * _bias
	#print(_low, _high, _loc, _bias)
	if meanValue > _high:
		meanValue = _high
	if meanValue < _low:
		meanValue = _low
	'''
	if meanValue > _loc:
		meanValue -= LOSS_VALUE
	elif meanValue < _loc:
		meanValue += LOSS_VALUE
	'''
	#print(meanValue)
	sigma = meanValue * 0.2 / 6
	if _bias != 1.0:
		print(_bias, "****")
	normalList = numpy.random.normal(loc = meanValue, scale = sigma, size = 2000)
	#intervalList = [i for i in normalList if i >= _low and i <= _high]
	#print(len(normalList))
	intervalList = normalList[numpy.where(normalList >= _low)]
	#print(len(intervalList))
	intervalList = intervalList[numpy.where(intervalList <= _high)]
	#添加涨跌值
	#intervalList = numpy.append(intervalList, [_low, _high])
	return intervalList

def getNormalList(_low, _high, _loc):
	#该函数生成一个符合正态分布的，值在[_low, _high]之间的序列
	normalList = numpy.random.normal(loc = _loc, scale = SIGMA, size = 300)
	#intervalList = [i for i in normalList if i >= _low and i <= _high]
	intervalList = normalList[numpy.where(normalList >= _low)]
	intervalList = intervalList[numpy.where(intervalList <= _high)]
	#添加涨跌值
	#intervalList = numpy.append(intervalList, [_low, _high])
	return intervalList

def getPrice(_low, _high, _price, _bias, _coolingValue):
	#该函数返回一个在[_low, _high]之间的浮点数，闭区间
	#生成符合正态分布的数列
	#要抑制偏移的幅度
	#_bias /= 3
	#正常情况下，_bias是0.9-1.1之间的数字
	_bias = 1
	priceList = getNormalListBias(_low, _high, _price, _bias, _coolingValue)
	count = 0
	while len(priceList) == 0:
		#print("\r计算正态分布中...", end = "")
		count += 1
		priceList = getNormalListBias(_low, _high, _price, _bias)
		if count >= 10000:
			print("%.2f %.2f %.2f %.1f" % (_low, _high, _price, _bias))
			while len(priceList) <= 100:
				tempNum = random.uniform(_low, _high + LOSS_VALUE)
				if tempNum >= _high:
					tempNum = _high
				priceList = numpy.append(priceList, tempNum)
	#print("\n%d" % count)
	#提取价格
	#print(len(priceList), "****")
	price1 = numpy.random.choice(priceList)
	price2 = numpy.random.choice(priceList)
	#判断价格边界，已经符合价格边界
	return price1, price2
	'''
	normalObj = st.truncnorm(lowerLimit, upperLimit, loc = _price, scale = SIGMA)
	#为有足够的挑选范围，生成长度为10000的数组
	normalList = list(normalObj.rvs(NORMAL_LIST_LENGTH))
	#排序
	normalList.sort()
	#然后随机挑选
	price1 = normalList[random.randint(0, NORMAL_LIST_LENGTH - 1)]
	if price1 > _high:
		price1 = _high
	elif price1 < _low:
		price1 = _low
	price2 = normalList[random.randint(0, NORMAL_LIST_LENGTH - 1)]
	if price2 > _high:
		price2 = _high
	elif price2 < _low:
		price2 = _low
	return price1, price2
	'''

'''
注意，好像没有更新出价范围--要根据交易调整实时调整出价范围
注意，涨跌停也没做--再完善--Done
'''
#_flag用于在初始化阶段忽视涨跌停规则，另外，不打印
def doTransaction(_accountsList, \
				  _user1Index, \
				  _user2Index, \
				  _sharesList, \
				  _shareIndex, \
				  _transactionRecord,
				  _flag,
				  _normalVolume):
	#双方先出价
	#获得出价区间
	lowLimit, highLimit = _sharesList[_shareIndex].getLimitRange()
	price = _sharesList[_shareIndex].getPrice()
	#获得持续增长/跌幅的天数的冷却值
	coolingValue = _sharesList[_shareIndex].getCoolingValue()
	'''
	if _flag == 1:
		print(coolingValue, "*****")
	'''
	#然后买方卖方出价
	#买方
	#注意，uniform函数只包含下限，不包含上限
	#要注意出价主要集中在中间，而不在两边—待完成——完成
	user1Price, user2Price = getPrice(lowLimit, highLimit, price, _normalVolume[_shareIndex] , coolingValue)
	#user2Price = getPrice(lowLimit, highLimit, price)
	#只有买方出价大于等于卖方要价时，才交易
	if user1Price >= user2Price:
		#交易
		#计算买卖的股数
		#有整取整，无整卖零
		#注意，买卖的股票数量不能多于卖方持有的数量
		num = _accountsList[_user1Index].howManySharesICanBuy(user1Price)
		num = min(num, _accountsList[_user2Index].howManySharesIHold(_shareIndex))
		#如果小于等于最小交易数
		if num <= LEAST_NUM:
			#全部买了
			#一个加钱减股票，一个减钱加股票
			_accountsList[_user1Index].buyShares(num, user1Price, _shareIndex)  
			_accountsList[_user2Index].sellShares(num, user1Price, _shareIndex)
			#最后调整价格
			if _flag:
				_sharesList[_shareIndex].setPrice(user1Price, _flag)
			#然后记录交易
			'''
			if _flag == 1:
				print("发生交易: 账户%d从账户%d买入第%d只股票交易%d股，买方出价-%.2f，卖方出价-%.2f, 交易价格-%.2f，该只股票出价范围-[%.2f, %.2f, %.2f，%.2f, %.2f]:" % (_user1Index + 1, _user2Index + 1, _shareIndex + 1, num, user1Price, user2Price, user1Price, _sharesList[_shareIndex].getLimitRange()[0], _sharesList[_shareIndex].getBidRange()[0], _sharesList[_shareIndex].getPrice(), _sharesList[_shareIndex].getBidRange()[1], _sharesList[_shareIndex].getLimitRange()[1]))
			'''
			_transactionRecord.newTransactionComes(_shareIndex, num)
			return
		else:	
			#买随机的整股数
			#该函数生成[LEAST_NUM, num]间的，步长为100的随机数
			roundSum = random.randrange(LEAST_NUM, num, LEAST_NUM)	
			_accountsList[_user1Index].buyShares(roundSum, user1Price, _shareIndex) 
			_accountsList[_user2Index].sellShares(roundSum, user1Price, _shareIndex)
			#然后记录交易
			'''
			if _flag == 1:
				print("发生交易: 账户%d从账户%d买入第%d只股票交易%d股，买方出价-%.2f，卖方出价-%.2f, 交易价格-%.2f，该只股票出价范围-[%.2f, %.2f, %.2f，%.2f, %.2f]:" % (_user1Index + 1, _user2Index + 1, _shareIndex + 1, roundSum, user1Price, user2Price, user1Price, _sharesList[_shareIndex].getLimitRange()[0], _sharesList[_shareIndex].getBidRange()[0], _sharesList[_shareIndex].getPrice(), _sharesList[_shareIndex].getBidRange()[1], _sharesList[_shareIndex].getLimitRange()[1]))
			'''
			_transactionRecord.newTransactionComes(_shareIndex, roundSum)
			#最后调整价格
			if _flag:
				_sharesList[_shareIndex].setPrice(user1Price, _flag)
			return
	else:
		#否则直接不做什么，返回
		return


if __name__ == "__main__":
	a = 20
	upperLimit = a * 1.1
	lowerLimit = a * 0.9
	middleCount = 0
	properCount = 0
	aList = getNormalListBias(lowerLimit, upperLimit, a, 1, 1)
	for i in aList:
		if i >= (a - (a * 0.2 / 6)) and i <= (a + (a * 0.2 / 6)):
			middleCount += 1
		if i >= a - 1 and i <= a + 1:
			properCount += 1
		else:
			continue
	print(middleCount / len(aList))
	print(properCount / len(aList))
	'''
	stime = time.time()
	bigCount = 0
	smallCount = 0
	middleCount = 0
	#for j in range(1, 11):
	for i in range(100000):
		print("\r%d" % i, end = " ")
		price = getPrice(lowerLimit, upperLimit, a, 1, 1)
		if price[0] >= (a - (a * 0.2 / 6)) and price[0] <= (a + (a * 0.2 / 6)):
			middleCount += 1
		if price[0] < a:
			smallCount += 1
		if price[0] > a:
			bigCount += 1																														
		if math.isclose(price[0], upperLimit):
			print(price[0], "涨停")
		elif math.isclose(price[0], lowerLimit):
			print(price[0], "跌停")
		else:
			continue
	etime = time.time()
	print(etime - stime)
	print(bigCount, smallCount)
	print("*" * 30)
	print(middleCount / 100000)
	'''