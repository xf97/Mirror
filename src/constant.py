#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
镜像系统的常量文件
'''

import json

SELL_PROB = 0.5	#卖出概率
UPPER_LIMIT = 1.1 #涨停
LOWER_LIMIT = 0.9 #跌停
BIAS_UPPER_LIMIT = 0.5	#偏移上限值
BIAS_LOWER_LIMIT = -0.5	#偏移下限值
DATA_PATH = "..\\data\\DataRequiredForMirror.xlsx"
INIT_PRICE = "initPrice"	#初始价格表名
PURCHASE_PROB = "purchaseProb"	#购买概率表名
SHARE_NUMBER = "initFund"	#初始股票数量
MIN_BUY_QUA = 100	#最小买入数量
LOSS_VALUE = 1e-10	#适当损失，用于在归一化时进一步收窄，避免触发涨跌停
ONE_FOURTH_PERIOD = 0.05	#允许连续增长或下跌的周期（价格增长或降幅），超过该值则冷却值变号
USERS_NEEDS_PATH = "..\\userNeeds.json"	#用户配置文档

def getUserNeeds():
	with open(USERS_NEEDS_PATH, "r", encoding = "utf-8") as f:
		text = f.read()
		#要清洗换行符号
		text = text.replace("\n", "")
		return json.loads(text)
	return str()

userNeeds = getUserNeeds()

INIT_TRANS_DAYS = 20 #初始化天数 
LAST_YEARS = userNeeds["LAST_YEARS"]	# 持续调查17年
USERS_NUM = userNeeds["USERS_NUM"] 	#参与账户数量
SHARES_NUM = userNeeds["SHARES_NUM"]	#参与的股票数量
DAYS_IN_1_YEAR = 247	#一年平均有247天交易日
DAYS_IN_1_MONTH = [20, 35, 58, 78, 98, 119, 142, 164, 185, 202, 224, 247] 	#每月最后一个交易日
SALE_PROBABILITY = 0.5	#想出售的概率