import numpy as np
import datetime
import random
from math import exp
import matplotlib.pyplot as plt

#################### GLOBAL VARIABLES ####################
g_nbYear = 5
g_nbDaysPerYear = 364
g_n = g_nbYear * g_nbDaysPerYear
g_dt = 1/g_nbDaysPerYear

# building list of dates
base = datetime.datetime.strptime("25-11-2022", "%d-%m-%Y")
calendar = [base - datetime.timedelta(days=x) for x in range(g_n)]
calendar.reverse()
###########################################################

# lambda function generating a geometrical brownian motion
gbm = lambda x, drift, volatility: x * exp((drift - volatility**2 / 2)*g_dt + volatility*np.sqrt(g_dt)*np.random.normal(0,1))

def normalize(liste):
    r = list()
    for e in liste:
        r.append(e*100/sum(liste))
    return r


####################### CLASS ASSET #######################
class Asset:
    def __init__(self, type, ticker, dictHistory = {}):
        self.type = type                # string
        self.ticker = ticker            # string
        self.dictHistory = dictHistory  # dict

    def generateHistory(self, drift, volatility):
        # Generates a random history based on drift and volatility given in parameters
        # To be replaced by a function retrieving the real history of the stock.
        prices = [1]
        for i in range(g_n - 1):
            prices.append(gbm(prices[-1], drift, volatility))
        dictHistory = dict(zip(calendar, prices))
        self.dictHistory = dictHistory

    def display(self, showPlot = False):
        print(self.type, self.ticker)
        #for keys, values in self.dictHistory.items():
            #print(keys.strftime("%d-%m-%Y"), values)
        if showPlot:
            plt.plot(self.dictHistory.keys(), self.dictHistory.values())
            plt.title(self.ticker)
            plt.show()

####################### CLASS STRATEGY #######################
class Strategy():
    def __init__(self, name, assets, dictInvestment = {}, performance = {}):
        self.name = name                # string
        self.assets = assets            # list of assets
        self.dictInvestment = dictInvestment  # dict
        self.performance = performance  # dict

    def generateInvestment(self):
        # Generates a random investment strategy. To be replaced by machine learning investment decisions.
        opening = random.sample(range(0, 100), len(self.assets))
        dailyInvestments = [normalize(opening)]
        for i in range(g_n):
            if random.randint(1,10) > 7:
                dailyInvestment = random.sample(range(0, 100), len(self.assets))
                dailyInvestments.append(normalize(dailyInvestment))
            else:
                dailyInvestments.append(dailyInvestments[-1])
        dictInvestment = dict(zip(calendar, dailyInvestments))
        self.dictInvestment = dictInvestment

    def computePerformance(self):
        markToMarket = [100]
        for day in calendar[0:g_n-1]:
            nextDay = day + datetime.timedelta(days=1)
            tempDict = dict(zip(self.assets, self.dictInvestment[day]))
            totalCashReturn = 0
            for asset, assetCashExposure in tempDict.items():
                assetDailyReturn = asset.dictHistory[nextDay]/asset.dictHistory[day]
                totalCashReturn += assetDailyReturn*assetCashExposure
            markToMarket.append(markToMarket[-1]*totalCashReturn/100)
        self.performance = markToMarket

    def display(self, showPlot = False):
        print(self.name)
        if showPlot:
            plt.plot(self.dictInvestment.keys(), self.performance)
            plt.title(self.name)
            plt.show()
        #for asset in self.assets:
            #asset.display()
        #for keys, values in self.dictInvestment.items():
            #print(keys.strftime("%d-%m-%Y"), values)

##########################################################


apple = Asset("stock", "AAPL")
apple.generateHistory(0.02, 0.1)
#apple.display(False)

amazon = Asset("stock", "AMZN")
amazon.generateHistory(0.015, 0.15)
#amazon.display(False)

total = Asset("stock", "TTE")
total.generateHistory(0.01, 0.08)
#total.display(False)

baba = Asset("stock", "BABA")
baba.generateHistory(0.025, 0.05)
#baba.display(False)

eurusd = Asset("Currency", "EUR/USD")
eurusd.generateHistory(0, 0.035)
#eurusd.display(False)

assets = list()
assets.append(apple)
assets.append(amazon)
assets.append(total)
assets.append(baba)
assets.append(eurusd)

myStrategy = Strategy("myStrategy", assets)
myStrategy.generateInvestment()
myStrategy.computePerformance()
myStrategy.display(True)


