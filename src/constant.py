#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
镜像系统的常量文件
'''

SELL_PROB = 0.5	#卖出概率
UPPER_LIMIT = 1.1 #涨停
LOWER_LIMIT = 0.9 #跌停
DATA_PATH = "..\\data\\dataForExp.xlsx"
INIT_PRICE = "initPrice"	#初始价格表名
PURCHASE_PROB = "purchaseProb"	#购买概率表名
SHARE_NUMBER = "initFund"	#初始股票数量
MIN_BUY_QUA = 100	#最小买入数量
LOSS_VALUE = 1e-5	#适当损失，用于在归一化时进一步收窄，避免触发涨跌停