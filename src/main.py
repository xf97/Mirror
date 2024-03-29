#!/usr/bin/python3

'''
这是Mirror镜像系统主控文件
用于调动各个组件用以驱动程序
python version: 3.7
'''

#导入库
import os
import logging
import rich	#定制化输出
import random
import openpyxl	#操作ecxel文件
import math
#账户数据结构，股票数据结构，每日交易信息保存数据结构，年报数据结构，常量
from account import accountClass as ac
from share import shareClass as sc
from transaction import transactionClass as tc
from annualReport import annualReportClass as arc
from constant import *
#交易函数
from makeDeals import *
#归一化公式
from normalization import *
#excel读写类
from excel2Dict import ExcelToDict
from dict2Excel import *

#常量部分
'''
INIT_TRANS_DAYS = 20 #初始化天数 
LAST_YEARS = 17	# 持续调查17年
USERS_NUM = 50	#参与账户数量
SHARES_NUM = 10	#参与的股票数量
DAYS_IN_1_YEAR = 247	#一年平均有247天交易日
DAYS_IN_1_MONTH = [20, 35, 58, 78, 98, 119, 142, 164, 185, 202, 224, 247] 	#每月最后一个交易日
SALE_PROBABILITY = 0.5	#想出售的概率
'''
#需要读取的数据文件们, 例如股票的信息, 年报的信息

class mirror:
	def __init__(self):
		#首先要初始化账户和股票
		#然后要初始化每只股票的年报信息以及股票
		#一次性获取每只股票20年的信息了，后面从里面查就好了
		#用不上
		#self.annualReportDict = self.initAnnualReports(SHARES_NUM)
		self.initFund = 0	#每个人持有的初始资金
		self.sharesList = self.initShares(SHARES_NUM)
		self.accountsList = self.initAccounts_1(USERS_NUM, self.initFund, self.sharesList)
		self.transactionRecord = tc(SHARES_NUM)	#交易记录
		self.initAccounts_2(INIT_TRANS_DAYS)
		#初始化日志记录
		#todo


	def initShares(self, _sharesNum):
		print("\rStock...ing", end = "")
		#初始化每只股票，包括价格、价格上下限、总股数、想买的概率(20年的，以数组形式)、当日是否允许再交易(涨跌停)
		#价格，id，总数和股票数量
		shareInfo = ExcelToDict(DATA_PATH)
		shareInfo.open_object()
		shareInfo.read_excel()
		#初始价格表
		initPriceSheet = shareInfo.data_dict[INIT_PRICE]
		purchaseProbSheet = shareInfo.data_dict[PURCHASE_PROB]
		shareNumberSheet = shareInfo.data_dict[SHARE_NUMBER]
		#股票信息字典，键-id，值-列表，依次是初始价格、股票总数、想买概率列表
		shareInfoDict = dict()
		for value in initPriceSheet["value_row"].values():
			shareId = value["StockId"]
			sharePrice = value["Price"]
			shareInfoDict[shareId] = list()
			shareInfoDict[shareId].append(sharePrice)
		#记录股票总数
		for index, value in enumerate(shareNumberSheet["value_row"].values()):
			if value and index < SHARES_NUM:
				shareId = int(value["StockId"])
				shareNum = int(value["NumberOfShares"])
				if self.initFund == 0:
					self.initFund = int(value["Cash"])
				shareInfoDict[shareId].append(shareNum)
		#初始化交易概率
		for valueDict in purchaseProbSheet["value_row"].values():
			shareId = list(valueDict.values())[0]
			sharePurcProbList = list(valueDict.values())[1:]
			shareInfoDict[int(shareId)].append(sharePurcProbList)
		#现在初始化股票
		sharesList = list()
		for key, value in shareInfoDict.items():
			#print(value)
			if value != [None]:
				shareId = key
				sharePrice = value[0]
				shareNumber = value[1]
				sharePurcProbList = value[2]
				sharesList.append(sc(sharePrice, shareNumber, sharePurcProbList, shareId))
		'''
		for obj in sharesList:
			print(obj)
		'''
		print("\rStock...Done")
		return sharesList

	def initAccounts_1(self, _accountsNum, _initFund, _sharesList):
		print("\rAccount...ing", end = "")
		#初始化每个账户，包括现有资金、13只股票的持有情况、利息账户
		accountsList = list()
		#要每只股票的总股数和价格
		shareInfoList = [[0, 0]] * len(_sharesList)
		for obj in _sharesList:
			shareId = obj.getShareId()
			shareNum = obj.getNumberOfShare()
			sharePrice = obj.getPrice()
			shareInfoList[shareId - 1] = [shareNum, sharePrice]
		#每次初始化两个用户，前一个初始化资金不足的由第二个补上
		i = 1
		while i <= _accountsNum:
			account1Ratio = random.randint(0, 100)	#账户1用来购买股票的资金比例
			account2Ratio = min(100, 100.1 - account1Ratio) 	#账户2用来购买股票的资金比例
			#print(account1Ratio, account2Ratio, account1Ratio + account2Ratio)
			account1 = ac(i , self.initFund, shareInfoList)	#账户1
			account2 = ac(i + 1, self.initFund, shareInfoList)	#账户2
			#出资购买股票，返回值是新的shareInfoList
			shareInfoList = account1.initHoldShares(account1Ratio, shareInfoList)
			shareInfoList = account2.initHoldShares(account2Ratio, shareInfoList)
			#把两个对象加入账户列表
			accountsList.append(account1)
			accountsList.append(account2)
			i += 2
		#print([i[0] for i in shareInfoList])
		'''
		for i in accountsList:
			print(i)
		'''
		return accountsList

	#自动交易以进一步分配股票和资金
	def initAccounts_2(self, _days):
		#初始化阶段无需更新涨跌停，也无需关心出范围
		#print("hahah")
		nowDay = 1
		normalizationVolume = [1.0] * len(self.sharesList)
		while nowDay <= _days:
			#print(nowDay)
			#对于每一个账户
			for userIndex in range(len(self.accountsList)):
				#对于每位用户
				shareIndexList = list(range(len(self.sharesList)))
				random.shuffle(shareIndexList)	#随机打乱顺序
				for shareIndex in shareIndexList:
					#对于每只股票
					#想买吗
					if random.random() < self.sharesList[shareIndex].getPurchaseProb(0):
						#想买
						#去问其他账户
						for anotherUserIndex in range(len(self.accountsList)):
							if anotherUserIndex == userIndex:
								#不跟自己做交易
								continue
							else:
								#找到持有这只股票的账户
								if self.accountsList[anotherUserIndex].doIOwnThisStock(shareIndex):
									#然后看这个账户想不想卖这只股票
									if random.random() < SELL_PROB:
										#想卖
										#那么进入买方卖方出价环节
										#要有交易记录的
										#买方账户、卖方账户、交易记录
										#直接在原数据上修改
										#print(1)
										doTransaction(self.accountsList, userIndex, anotherUserIndex, self.sharesList, shareIndex, self.transactionRecord, 0, normalizationVolume)
										#print(2)
									else:
										#不想卖
										continue
								else:
									continue
					else:
						#不想买，去问其他股票
						continue
			process = int(nowDay / _days * 100)
			#print(process)
			print("\rAccount:" + str(process) +"%", end = "")
			nowDay += 1
			#更新交易记录
			self.transactionRecord.newDayComes()
		print("\n")
		#清空交易记录
		self.transactionRecord.clear()

	def initAnnualReports(self, _sharesNum):
		#暂不需要
		#初始化每只股票各自的20年的年报，使用这些信息计算股票的信息(第一年的基础价格,
		#后续每年的想买概率)
		pass

	def updateShares(self, _annualReports, _nowYear):
		#暂不需要
		#根据当前年份，更新股票的数据
		pass

	'''
	可能需要引入numpy来返回符合正态分布的数据，来增大出价不触发涨停的概率
	'''
	def run(self):
		#进行交易
		nowYear = 1	#当前年份
		nowDay = 1	#当前天数
		nowMonth = 1	#当前月份
		#信息记录字典
		infoDict = dict()	#键是月份，值是当月所有股票的收盘价，每年重置一次
		while nowYear <= LAST_YEARS:
			#每年开始，先记录当年的初始价格
			for share in self.sharesList:
				share.setNewYearPrice(share.getPrice())
			#模拟二十年的
			#print("*" * 20, str(nowYear) + " ", str(nowMonth) + " ", str(nowDay), "*" * 20)
			while nowDay <= DAYS_IN_1_YEAR:
				#对于一天来说，昨天的交易成交量是固定的
				#要记得挪动出价区间
				#先计算每个股票的相对成交量
				#获得昨日平均成交量
				aveShareNum = self.transactionRecord.getYesterdayAveTransNum()
				if math.isclose(aveShareNum, 1):
					#第一天，昨日无成交
					normalizationVolume = [0.0] * len(self.sharesList)	#就在原值进行改动
				else: 
					relativeVolumeList = [0.0] * len(self.sharesList)
					#更新aveShareNum，使用钱来投票
					aveShareNum = 0.0
					for index, share in enumerate(self.sharesList):
						#获得昨日交易量
						thisShareNum = self.transactionRecord.getYesterdayTransNum(index)
						#获得昨日价格
						prePrice = share.prePrice
						#加上
						aveShareNum += (thisShareNum * prePrice)
					#计算平均
					aveShareNum /= (len(self.sharesList))
					#计算归一化
					for index, share in enumerate(self.sharesList):
						#获得该只股票昨日交易量
						thisShareNum = self.transactionRecord.getYesterdayTransNum(index)
						#获得昨日价格
						prePrice = share.prePrice
						#计算相对成交量
						relativeVolumeList[index] = (thisShareNum * prePrice) / aveShareNum
					#然后对相对成交量进行一个归一化处理
					#不在原值上修改，要保留变量
					#print(relativeVolumeList)
					normalizationVolume = normalization(relativeVolumeList, BIAS_UPPER_LIMIT, BIAS_LOWER_LIMIT)
				#print(normalizationVolume)
				#对于每一个账户
				for userIndex in range(len(self.accountsList)):
					#对于每位用户					
					shareIndexList = list(range(len(self.sharesList)))
					random.shuffle(shareIndexList)	#随机打乱顺序
					for shareIndex in shareIndexList:
						#对于每只股票
						#今天还可以买吗-有没有被前面的人所买涨跌停了
						if self.sharesList[shareIndex].getStopFlag() == True:
							continue
						#想买吗
						#买卖的过程中，会导致涨跌停
						if random.random() < self.sharesList[shareIndex].getPurchaseProb(nowYear - 1):
							#print("第%d只股票的交易概率-%.2f" % (shareIndex + 1, self.sharesList[shareIndex].getPurchaseProb(nowYear - 1)))
							#想买
							#去问其他账户
							for anotherUserIndex in range(len(self.accountsList)):
								if self.sharesList[shareIndex].getStopFlag() == True:
									#print("今日第%d只股票交易已经锁止" % (shareIndex + 1))
									#股票锁止，今日该股票的交易
									break
								if anotherUserIndex == userIndex:
									#不跟自己做交易
									continue
								else:
									#找到持有这只股票的账户
									#一次交易过程中会发生涨跌停
									if self.accountsList[anotherUserIndex].doIOwnThisStock(shareIndex):
										#然后看这个账户想不想卖这只股票
										if random.random() < SELL_PROB:
											#想卖
											#那么进入买方卖方出价环节
											#要有交易记录的
											#买方账户、卖方账户、交易记录
											#直接在原数据上修改
											doTransaction(self.accountsList, userIndex, anotherUserIndex, self.sharesList, shareIndex, self.transactionRecord, 1, normalizationVolume)
											#注意，这个过程会触发涨跌停
										else:
											#不想卖
											continue
									else:
										continue
						else:
							#不想买，去问其他股票，或者已经涨跌停
							continue
				#根据交易记录调整价格
				#print("调整价格")
				#调整单调天数
				for share in self.sharesList:
					share.dailyInit()
				for index, share in enumerate(self.sharesList):
					#print("第%d只股票，前天收盘价-%.2f,今天收盘价-%.2f,共交易%d笔,当前冷却因子%.2f,当前偏移值%.2f" % (share.getShareId(), share.prePrice, share.price, self.transactionRecord.getHandCount(index), share.getCoolingValue(share.price), normalizationVolume[index]))
					#print("%d# Stock，yesterday price-%.2f, today price-%.2f, total transaction %d, current cold value %.2f, current bias value %.2f" % (share.getShareId(), share.prePrice, share.price, self.transactionRecord.getHandCount(index), share.getCoolingValue(share.price), normalizationVolume[index]))
					print("%d# Stock，yesterday price-%.2f, today price-%.2f, total transaction %d" % (share.getShareId(), share.prePrice, share.price, self.transactionRecord.getHandCount(index)))
				#记录当天收盘价
				for share in self.sharesList:
					share.setPrePrice()
				'''
				for index, share in enumerate(self.sharesList):
					#如果达到涨跌停值，那么第二天开盘价格就是这个涨跌停值
					if share.getStopFlag() == True:
						#重置价格，重置涨跌停标志，重置出价上下限
						share.dailyInit(share.getPrice())
					else:
						#否则根据相对交易量，计算涨跌额度
						share.dailyInit(share.getPrice() * normalizationVolume[index])
				'''
				#更新交易记录
				self.transactionRecord.newDayComes()
				print("*" * 20, str(nowYear) + " Year ", str(nowMonth) + " Month ", str(nowDay), " Day ", "*" * 20)
				if nowDay == DAYS_IN_1_MONTH[nowMonth - 1]:
					#达到当月最后一天
					#记录数据
					infoDict[nowMonth] = [share.getPrice() for share in self.sharesList]
					nowMonth += 1	
				nowDay += 1
			#一年结束
			#记录本年数据
			dict2Excel(nowYear, infoDict, SHARES_NUM, "Month/Stock")
			nowYear += 1
			nowDay = 1
			nowMonth = 1
			#然后置空	
			infoDict.clear()
		#看看交易后能不能把账户数据打出来
		for account in self.accountsList:
			print(account)
		#股票交易数量
		print([int(i) for i in self.transactionRecord.getTotalTransactionNum()])


#单元测试
if __name__ == "__main__":
	aMirror = mirror()
	aMirror.run()
