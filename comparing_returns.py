import pandas as pd
import pandas_datareader as web
import datetime
import numpy as np
import pyEX as p
iex_sandbox_key = 'Tpk_ec52cb37b61542d8b350bf9df129fcb5'

import get_csv_module
from create_portfolio_df import transformCSV, recalculateWeights



print("comparing_returns.py has loaded")

currentPortfolio = get_csv_module.CSVGetInfo("/Users/jackk/Projects/pythonProjects/PortfolioAnalysis/", "holdings_sample.csv")

get_csv_module.display_file_location(currentPortfolio.path, currentPortfolio.file_name)

##show inital columns in csv
currentPortfolio.display_summary()

##create dataframe and process data
portfolio_df = pd.read_csv(currentPortfolio.path + currentPortfolio.file_name)
portfolio_df = transformCSV(portfolio_df)

##check df transformed correctly
print(portfolio_df.head(10))

tickerList = portfolio_df['Symbol'].tolist()
print (tickerList)
weightList = portfolio_df['Weight'].tolist()
print(weightList)

end = datetime.datetime(2021,7,1)
start = datetime.datetime(2021,6,1)

##start with index, match symbol to weight later
def PortfolioWeeklyReturns(symbolList, weightList, IEXobject):
    returnList = []
    i = 0
    for symbol in symbolList:
        symbolReturns = getWeeklyReturns(symbol, IEXobject)
        ##print(symbolReturns)
        for profit in symbolReturns[1]:
            profit = profit * weightList[i]
        symbolReturns = symbolReturns[1]
        ##print(symbolReturns)
        i=i+1

        returnList = returnList + symbolReturns

    print("\n"+"\n"+"List of pertfolio returns is ", returnList)


    return returnList

def getWeeklyReturns(symbol, IEXobject):
    df = IEXobject.chartDF(symbol=symbol, timeframe='5y', interval = 5)[['close', 'volume']]
    maxIndex = len(df['close']) -1
    i=0
    profitList = []
    returnList = [symbol, profitList]

    while i < maxIndex:
        profit = df['close'][i] / df['close'][i+1] -1
        profitList.append(profit)
        i = i+1

    return returnList


##change from ticker objects to series objects
def ReturnStatistics(ticker1, ticker2, IEXobject):
##for finding the return statistics of a single ticker against a given benchmark
    testSeries = getWeeklyReturns(ticker1, IEXobject)
    testSeries = testSeries[1]
    testSeries = pd.Series(testSeries)

    benchmark = getWeeklyReturns(ticker2, IEXobject)
    benchmark = benchmark[1]
    benchmark = pd.Series(benchmark)

  ##return calculations, need to separate series of returns from symbol key in dictionary
    print("Correlation is ", testSeries.corr(benchmark, method = 'pearson', min_periods = 10))
    print("Covariance is ", testSeries.cov(benchmark, min_periods = 10, ddof = 1))

    return


##IEX Stock Price Return sourcing using pyEX library
c= p.Client(api_token = 'Tpk_ec52cb37b61542d8b350bf9df129fcb5', version = 'sandbox')
##ReturnStatistics("AAPL", "SPY", c)
PortfolioWeeklyReturns(tickerList, weightList, c)






##find weekly returns for companies in portfolio (Done) -->weighted average to find for portfolio
##regress/chart portfolio wwekly returns against sp500
##run portfolio return correlation to S&P500
##Out portfolio weekly VaR