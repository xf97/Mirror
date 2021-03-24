#!/usr/bin/python

'''
python version: 3.7

该类用于定义单个账户的数据结构
'''

from constant import *
import copy	#用于深度复制
import random

#常量
INC_FLAG = "+"
DEC_FLAG = "-"

class accountClass:
	#传入的
	def __init__(self, _accountId, _fund, _sharesInfoList):
		self.accountId = _accountId
		#所有数据的外部可见性先暂定为public
		self.fund = _fund	#持有的资金, 尚不明确是整型还是double
		self.stockHolding = [0] * len(_sharesInfoList)	#持有的股票, 列表第i位的数值表示该用户持有第i只股票的数量
		self.stockPriceAndNum = dict()
		self.interest = 0.0	#利息, 尚不明确该属性是否需要，暂不需要，但暂不删除

	def __str__(self):
		msg = str()
		msg += ("当前账户编号： " + str(self.accountId) + "\n")
		msg += ("当前资金： " + str(self.fund) + "\n")
		msg += ("股票持有情况： \n")
		for index, i in enumerate(self.stockHolding):
			if i != 0:
				msg += ("第" + str(index + 1) + "只： " + str(i) + "\n")
			else:
				continue
		return msg

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

	#_ratio指的是用多少资金购买股票
	#_shareInfoList指的是当前每只股票还可以购买的数量和价格
	#返回购买后的_sharesInfoList
	def initHoldShares(self, _ratio, _sharesInfoList):
		#先准备钱
		totalMoney = self.fund * (_ratio / 100)
		try:
			lowestPrice = min([i[1] for i in _sharesInfoList if i[0] > 0])
		except ValueError:
			lowestPrice = 0
		tempSharesInfoList = _sharesInfoList[:]
		index = 0	#买入股票的下标
		while totalMoney >= lowestPrice and index < len(_sharesInfoList):
			#当当前资金还够买入哪怕是一只股票时运行
			#先获得买当前这只股票的钱
			#print(tempSharesInfoList[index])
			if tempSharesInfoList[index][0] == 0:
				#卖完了
				index += 1	#去看下一只股票，钱不动
				continue
			else:
				nowMoney = totalMoney #* random.random()	#拿出一部分钱来买这只股票
				if index == self.getLastShareOnSale(tempSharesInfoList):
					#如果是最后一支没卖完的股票，就用所有钱买
					nowMoney = totalMoney
				#计算当前这些钱能买多少股票
				maxNum = (nowMoney // tempSharesInfoList[index][1])
				purchaseShareNum = min(maxNum, tempSharesInfoList[index][0])
				#决定了购买的数量
				#那么扣钱
				spendMoney = purchaseShareNum * tempSharesInfoList[index][1]
				totalMoney -= spendMoney
				self.setFund(spendMoney, DEC_FLAG)
				#self.fund -= spendMoney
				self.stockHolding[index] = purchaseShareNum
				tempSharesInfoList[index][0] -= purchaseShareNum
				index += 1
				try:
					lowestPrice = min([i[1] for i in tempSharesInfoList if i[0] > 0])
				except ValueError:
					continue
		#print(self.fund, self.stockHolding)
		#print("*" * 20)
		return tempSharesInfoList

	#传入股票列表，返回最后一只在售股票的下标
	def getLastShareOnSale(self, _shareInfoList):
		#从后向前遍历
		for index, share in enumerate(_shareInfoList[::-1]):
			if share[0] != 0:
				return len(_shareInfoList) - index - 1
			else:
				continue
			return -1

	#返回该用户持有第_index只股票吗
	def doIOwnThisStock(self, _index):
		return self.stockHolding[_index] != 0




