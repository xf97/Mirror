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
#账户数据结构，股票数据结构，每日交易信息保存数据结构，年报数据结构
from account import accountClass as ac
from share import shareClass as sc
from transaction import transactionClass as tc
from annualReport import annualReportClass as arc

#常量部分
LAST_YEARS = 20	# 持续调查20年
USERS_NUM = 50	#参与账户数量
SHARES_NUM = 50	#参与的股票数量
DAYS_IN_1_YEAR = 360	#一年按360天计算，便于生成每月记录
DAYS_IN_1_MONTH = 30 	#每月的天数
SALE_PROBABILITY = 0.5	#想出售的概率
#需要读取的数据文件们, 例如股票的信息, 年报的信息

class mirror:
	def __init__(self):
		#首先要初始化账户和股票
		self.accountsList = self.initAccounts(USERS_NUM, SHARES_NUM)
		#然后要初始化每只股票的年报信息以及股票
		#一次性获取每只股票20年的信息了，后面从里面查就好了
		self.annualReportDict = self.initAnnualReports(SHARES_NUM)
		self.sharesList = self.initShares(SHARES_NUM, self.annualReportDict)
		#初始化日志记录
		#todo
		pass

	def initShares(self, _sharesNum):
		#初始化每只股票，包括价格、价格上下限、总股数、想买的概率(20年的，以数组形式)、当日是否允许再交易(涨跌停)
		pass

	def initAccounts(self, _accountsNum, _sharesNum):
		#初始化每个账户，包括现有资金、50只股票的持有情况、利息账户
		pass

	def initAnnualReports(self, _sharesNum):
		#初始化每只股票各自的20年的年报，使用这些信息计算股票的信息(第一年的基础价格,
		#后续每年的想买概率)
		pass

	def updateShares(self, _annualReports, _nowYear):
		#根据当前年份，更新股票的数据
		pass

	def run(self):
		#进行交易
		nowYear = 1	#当前年份
		nowDay = 1
		while nowYear <= LAST_YEARS:
			#模拟二十年的
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
		print("Done")