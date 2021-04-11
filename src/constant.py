#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
镜像系统的常量文件
'''

SELL_PROB = 0.5	#卖出概率
UPPER_LIMIT = 1.1 #涨停
LOWER_LIMIT = 0.9 #跌停
BIAS_UPPER_LIMIT = 1.0	#偏移上限值
BIAS_LOWER_LIMIT = -1.0	#偏移下限值
DATA_PATH = "..\\data\\dataForExp.xlsx"
INIT_PRICE = "initPrice1"	#初始价格表名
PURCHASE_PROB = "purchaseProb2"	#购买概率表名
SHARE_NUMBER = "initFund2"	#初始股票数量
MIN_BUY_QUA = 100	#最小买入数量
LOSS_VALUE = 1e-10	#适当损失，用于在归一化时进一步收窄，避免触发涨跌停
ONE_FOURTH_PERIOD = 5	#允许连续增长或下跌的周期，超过该值则冷却值变号
