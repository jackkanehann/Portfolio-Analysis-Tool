import pandas as pd
import numpy as np
import pandas_datareader as web
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.stats import norm
from tabulate import tabulate
import pyEX as p

##sandbox API key, so no fees for historical data
iex_sandbox_key = 'Tpk_ec52cb37b61542d8b350bf9df129fcb5'

import get_csv_module
from create_portfolio_df import transformCSV, recalculateWeights

def PortfolioDailyReturns(symbolList, weightList, IEXobject):
    returnList = []
    i = 0
    for symbol in symbolList:
        symbolReturns = getDailyReturns(symbol, IEXobject)
        for profit in symbolReturns[1]:
            profit = profit * weightList[i]

        ##adjust 504 to 252*years of returns-- 252, 504, 756, 1008, 1260 etc.
        while len(symbolReturns[1]) < 1260:
            symbolReturns[1].append(0)
        symbolReturns = np.array(symbolReturns[1])
        i=i+1

        ##careful to sum array elements, not concatenated arrays
        if returnList.size == 0:
            returnList = symbolReturns
        else:
            returnList = returnList + symbolReturns

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

def getDailyReturns(symbol, IEXobject):
    df = IEXobject.chartDF(symbol=symbol, timeframe='5y', interval = 1)[['close', 'volume']]
    maxIndex = len(df['close']) -1
    i=0
    profitList = []
    returnList = [symbol, profitList]

    while i < maxIndex:
        profit = df['close'][i] / df['close'][i+1] -1
        profitList.append(profit)
        i = i+1

    return returnList

def getDailyLogReturns(symbol, IEXobject):
    df = IEXobject.chartDF(symbol=symbol, timeframe='5y', interval = 1)[['close', 'volume']]
    maxIndex = len(df['close']) -1
    i=0
    profitList = []
    returnList = [symbol, profitList]

    while i < maxIndex:
        profit = np.log(df['close'][i] / df['close'][i+1])
        profitList.append(profit)
        i = i+1

    return returnList

def PortfolioDailyLogReturns(symbolList, weightList, IEXobject):
    returnList = np.array([])
    i = 0
    for symbol in symbolList:
        symbolReturns = getDailyLogReturns(symbol, IEXobject)
        for profit in symbolReturns[1]:
            profit = profit * weightList[i]

        ##adjust 504 to 252*years of returns-- 252, 504. 756 etc.
        while len(symbolReturns[1]) < 1260:
            symbolReturns[1].append(0)
        symbolReturns = np.array(symbolReturns[1])
        i=i+1

        ##careful to sum array elements, not concatenated arrays
        if returnList.size == 0:
            returnList = symbolReturns
        else:
            returnList = returnList + symbolReturns

    return returnList

##change from ticker objects to series objects
def TickerReturnStatistics(ticker1, ticker2, IEXobject):
##for finding the return statistics of a single ticker against a given benchmark, need to separate series of returns from symbol key in dictionary
    testSeries = getDailyLogReturns(ticker1, IEXobject)
    testSeries = testSeries[1]
    testSeries = pd.Series(testSeries)

    benchmark = getDailyLogReturns(ticker2, IEXobject)
    benchmark = benchmark[1]
    benchmark = pd.Series(benchmark)

  ##return calculations
    print(ticker1, "Correlation with ", ticker2, " is ", testSeries.corr(benchmark, method = 'pearson', min_periods = 10))
    print(ticker1, "Covariance with ", ticker2, " is ", testSeries.cov(benchmark, min_periods = 10, ddof = 1))

    return

##change from ticker objects to series objects
def PortfolioReturnStatistics(portfolioReturns, ticker2, IEXobject):
##for finding the return statistics of a single ticker against a given benchmark
    testSeries = pd.Series(portfolioReturns)

    ## need to separate series of returns from symbol key in dictionary
    benchmark = getDailyLogReturns(ticker2, IEXobject)
    benchmark = benchmark[1]
    benchmark = pd.Series(benchmark)

  ## VGSH is Vanguard Short-Term Treasury Index Fund ETF, a proxy for the risk-free rate of return over a given period
    riskFreeSeries = getDailyLogReturns("VGSH", IEXobject)
    riskFreeSeries = riskFreeSeries[1]
    riskFreeSeries = pd.Series(riskFreeSeries)

    mean = np.mean(testSeries)
    std_dev = np.std(testSeries)
    VaR90 = norm.ppf(1-.90, mean, std_dev)
    VaR95 = norm.ppf(1-.95, mean, std_dev)
    VaR99 = norm.ppf(1-.99, mean, std_dev)

    SharpeRatioReturns = testSeries.subtract(riskFreeSeries, fill_value=0)
    SharpeRatioReturns = SharpeRatioReturns.sum()

    ##adjust to 1 / years of returns
    SharpeRatioReturns = pow(SharpeRatioReturns, 1/5)
    SharpeRatio = SharpeRatioReturns / std_dev

  ##return calculations
    print("Portfolio correlation with benchmark is ", testSeries.corr(benchmark, method = 'pearson', min_periods = 10))
    print("Portfolio covariance with benchmark is ", testSeries.cov(benchmark, min_periods = 10, ddof = 1))
    print("Portfolio Sharpe Ratio is ", SharpeRatio)
    print("Portfolio Total Return over the period is ", testSeries.sum())
    print("Benchmark Total Return over the period is ", benchmark.sum())
    print(tabulate([['Confidence Level', 'Value at Risk'], ['90%', VaR90], ['95%', VaR95], ['99%', VaR99]]))

    ##graph returns
    testSeries.hist(bins=40, histtype='stepfilled', alpha=0.5)
    x = np.linspace(mean-3*std_dev, mean + 3*std_dev, 100)
    plt.plot(x, norm.pdf(x, mean, std_dev),"r")
    plt.xlabel('Return %')
    plt.ylabel('Occurrences')
    plt.title("Normal Distribution of Portfolio Historic Returns")
    plt.legend()
    plt.show()

    testSeries = np.array(testSeries)
    benchmark = np.array(benchmark)

    ##graph portfolio returns vs benchmark returns
    x = np.linspace(0,testSeries.size, testSeries.size)
    plt.plot(x, testSeries,'bo', label = 'Portfolio Returns')
    xx = np.linspace(0,benchmark.size, benchmark.size)
    plt.plot(xx, benchmark, 'go', label = 'Benchmark Returns')
    plt.xlabel('Time in Days')
    plt.ylabel('Daily Return')
    plt.title("Comparing Returns")
    ##plt.legend()
    plt.show()


    return

print("comparing_returns.py has loaded")

if __name__ == "__main__":

    ##Grab CSV file using path + file name
    currentPortfolio = get_csv_module.CSVGetInfo("/Users/jackk/Projects/pythonProjects/PortfolioAnalysis/", "holdings_sample.csv")

    get_csv_module.display_file_location(currentPortfolio.path, currentPortfolio.file_name)

    ##show inital columns in csv
    currentPortfolio.display_summary()

    ##create dataframe and preprocess data
    portfolio_df = pd.read_csv(currentPortfolio.path + currentPortfolio.file_name)
    portfolio_df = transformCSV(portfolio_df)
    tickerList = portfolio_df['Symbol'].tolist()
    weightList = portfolio_df['Weight'].tolist()

    ##IEX Stock Price Return sourcing using pyEX library
    c= p.Client(api_token = 'Tpk_ec52cb37b61542d8b350bf9df129fcb5', version = 'sandbox')

    TickerReturnStatistics("AAPL", "MSFT", c)

    returnList = PortfolioDailyLogReturns(tickerList, weightList, c)
    PortfolioReturnStatistics(returnList ,"SPY", c)

"""
remember to adjust Sharpe Ratio, portfolio return functions, and daily return functions if
you want to analyze a different time period in years
""" 