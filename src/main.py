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
#账户数据结构，股票数据结构，每日交易信息保存数据结构，年报数据结构，常量
from account import accountClass as ac
from share import shareClass as sc
from transaction import transactionClass as tc
from annualReport import annualReportClass as arc
from constant import *
#交易函数
from makeDeals import *
#excel读写类
from excel2Dict import ExcelToDict


#常量部分
LAST_YEARS = 20	# 持续调查20年
USERS_NUM = 2	#500	#参与账户数量
SHARES_NUM = 50	#参与的股票数量
DAYS_IN_1_YEAR = 10 #239	#一年平均有239天交易日
DAYS_IN_1_MONTH = [10] * 10 #[19, 35, 57, 77, 95, 115, 137, 159, 179, 196, 217, 239] 	#每月最后一个交易日
SALE_PROBABILITY = 0.5	#想出售的概率
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
		self.accountsList = self.initAccounts(USERS_NUM, self.initFund, self.sharesList)
		self.transactionRecord = tc(SHARES_NUM)	#交易记录
		#初始化日志记录
		#todo

	def initShares(self, _sharesNum):
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
			shareId = value["股票代码"]
			sharePrice = value["初始价格"]
			shareInfoDict[shareId] = list()
			shareInfoDict[shareId].append(sharePrice)
		#记录股票总数
		for value in shareNumberSheet["value_row"].values():
			shareId = int(value["股票代码"])
			shareNum = int(value["初始股数"])
			if self.initFund == 0:
				self.initFund = int(value["初始资金"])
			shareInfoDict[shareId].append(shareNum)
		#初始化交易概率
		for valueDict in purchaseProbSheet["value_row"].values():
			shareId = list(valueDict.values())[0]
			sharePurcProbList = list(valueDict.values())[1:]
			shareInfoDict[int(shareId)].append(sharePurcProbList)
		#现在初始化股票
		sharesList = list()
		for key, value in shareInfoDict.items():
			shareId = key
			sharePrice = value[0]
			shareNumber = value[1]
			sharePurcProbList = value[2]
			sharesList.append(sc(sharePrice, shareNumber, sharePurcProbList, shareId))
		'''
		for obj in sharesList:
			print(obj)
		'''
		return sharesList

	def initAccounts(self, _accountsNum, _initFund, _sharesList):
		#初始化每个账户，包括现有资金、50只股票的持有情况、利息账户
		accountsList = list()
		#要每只股票的总股数和价格
		shareInfoList = [[0, 0]] * len(_sharesList)
		for obj in _sharesList:
			shareId = obj.getShareId()
			shareNum = obj.getNumberOfShare()
			sharePrice = obj.getPrice()
			shareInfoList[shareId - 1] = [shareNum, sharePrice]
		#每次初始化两个用户，前一个初始化资金不足的由第二个补上
		for i in range(_accountsNum // 2):
			account1Ratio = random.randint(0, 100)	#账户1用来购买股票的资金比例
			account2Ratio = min(100, 100.1 - account1Ratio) 	#账户2用来购买股票的资金比例
			#print(account1Ratio, account2Ratio, account1Ratio + account2Ratio)
			account1 = ac(i + 1, self.initFund, shareInfoList)	#账户1
			account2 = ac(i + 251, self.initFund, shareInfoList)	#账户2
			#出资购买股票，返回值是新的shareInfoList
			shareInfoList = account1.initHoldShares(account1Ratio, shareInfoList)
			shareInfoList = account2.initHoldShares(account2Ratio, shareInfoList)
			#把两个对象加入账户列表
			accountsList.append(account1)
			accountsList.append(account2)
		#print([i[0] for i in shareInfoList])
		'''
		for i in accountsList:
			print(i)
		'''
		return accountsList


	def initAnnualReports(self, _sharesNum):
		#暂不需要
		#初始化每只股票各自的20年的年报，使用这些信息计算股票的信息(第一年的基础价格,
		#后续每年的想买概率)
		pass

	def updateShares(self, _annualReports, _nowYear):
		#暂不需要
		#根据当前年份，更新股票的数据
		pass

	def run(self):
		#进行交易
		nowYear = 1	#当前年份
		nowDay = 1	#当前天数
		nowMonth = 1	#当前月份
		while nowYear <= 2:
			#模拟二十年的
			while nowDay <= DAYS_IN_1_YEAR:
				#对于每一个账户
				for userIndex in range(len(self.accountsList)):
					#对于每位用户
					for shareIndex in range(len(self.sharesList)):
						#对于每只股票
						#想买吗
						if random.random() < self.sharesList[shareIndex].getPurchaseProb(nowYear - 1):
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
											doTransaction(self.accountsList, userIndex, anotherUserIndex, self.sharesList, shareIndex, self.transactionRecord)
										else:
											#不想卖
											continue
									else:
										continue
						else:
							#不想买，去问其他股票
							continue
				if nowDay == DAYS_IN_1_MONTH[nowMonth - 1]:
					#达到当月最后一天
					#记录数据
					nowMonth += 1
				nowDay += 1
				#要记得挪动出价区间
				#更新交易记录
				self.transactionRecord.newDayComes()
				print(nowYear, nowMonth, nowDay)
			#一年结束
			nowYear += 1
			nowDay = 1
			nowMonth = 1
			'''
			if nowYear != 1:
				#第一年的数据已经初始化
				#初始化其他年的股票数据
				self.sharesList = self.updateShares(self.annualReportDict, nowYear)
			while nowDay <= 360:
				#开始模拟一年的交易
				#初始化当日交易记录数据存储结构
				if nowDay % DAYS_IN_1_MONTH == 0:
					#满一个月，记录当月的信息
					pass
				for userIndex in range(len(accountsList)):
					#对于每位用户
					for shareIndex in range(len(sharesList)):
						#对于每只股票
						#想买吗
						if random.random() < 该只股票的购买概率:
							#想买
							#那么询问除了他以外的所有人
							for anotherUserIndex in range(len(accountsList)):
								if anotherUserIndex == userIndex:
									#不跟自己交易
									continue
								else:
									#找到了别人，首先看这个人手上有没有持有
									if random.random() < SALE_PROBABILITY and 这个人手上有这只股票:
										#这个人有这只股票并且也想卖
										#那么出价
										#买方出价
										#卖方出价
										#比较，若买方>卖方, 成交
										#计算交易股数-受买方资金限制
										#扣除买方的资金，增加买方的该只股票
										#增加卖方的资金，扣除卖方的股票
										#记录交易
									else:
										continue
						else:
							#不想买这一只，去问其他股票
							continue
				#当天交易结束
				#汇总当天交易记录，可能要重新计算股价
				nowDay += 1
			#一年交易结束
			#汇总当年的交易记录，可能需要存盘
			nowYear += 1
		'''

#单元测试
if __name__ == "__main__":
	aMirror = mirror()
	aMirror.run()
