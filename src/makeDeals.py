#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
该文件用于编写用于交易的函数
从而将该函数从主文件中抽取出来
'''

__author__ = "xiaofeng"

#常量
#偏移值，用于包含随机数上限
STAND_BIAS = 0.1
#最小整笔交易数
LEAST_NUM = 100

#导入文件
import random
#账户数据结构，股票数据结构，每日交易信息保存数据结构，年报数据结构，常量
from account import accountClass as ac
from share import shareClass as sc
from transaction import transactionClass as tc
from annualReport import annualReportClass as arc
from constant import * 

'''
_user1是买方，_user2是卖方
买卖_shareIndex股票
交易的价格要在允许区间内
成交后价格需要记录和变动
成交的数据要记录
'''

def getPrice(_low, _high):
	#该函数返回一个在[_low, _high]之间的浮点数，闭区间
	price = random.uniform(_low, _high + STAND_BIAS)
	if price > _high:
		return _high
	else:
		return price

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
				  _flag):
	#双方先出价
	#获得出价区间
	lowLimit, highLimit = _sharesList[_shareIndex].getBidRange()
	#然后买方卖方出价
	#买方
	#注意，uniform函数只包含下限，不包含上限
	#要注意出价主要集中在中间，而不在两边—待完成！
	user1Price = getPrice(lowLimit, highLimit)
	user2Price = getPrice(lowLimit, highLimit)
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
			_sharesList[_shareIndex].setPrice(user1Price, _flag)
			#然后记录交易
			'''
			if _flag == 1:
				print("发生交易: 账户%d从账户%d买入第%d只股票交易%d股，买方出价-%.2f，卖方出价-%.2f, 交易价格-%.2f，该只股票出价范围-[%.2f, %.2f，%.2f]:" % (_user1Index + 1, _user2Index + 1, _shareIndex + 1, num, user1Price, user2Price, user1Price, _sharesList[_shareIndex].getBidRange()[0], _sharesList[_shareIndex].getPrice(), _sharesList[_shareIndex].getBidRange()[1]))
			_transactionRecord.newTransactionComes(_shareIndex, num)
			'''
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
				print("发生交易: 账户%d从账户%d买入第%d只股票交易%d股，买方出价-%.2f，卖方出价-%.2f, 交易价格-%.2f，该只股票出价范围-[%.2f, %.2f，%.2f]:" % (_user1Index + 1, _user2Index + 1, _shareIndex + 1, roundSum, user1Price, user2Price, user1Price, _sharesList[_shareIndex].getBidRange()[0], _sharesList[_shareIndex].getPrice(), _sharesList[_shareIndex].getBidRange()[1]))
			'''
			_transactionRecord.newTransactionComes(_shareIndex, roundSum)
			#最后调整价格
			_sharesList[_shareIndex].setPrice(user1Price, _flag)
			return
	else:
		#否则直接不做什么，返回
		return


if __name__ == "__main__":
	pass