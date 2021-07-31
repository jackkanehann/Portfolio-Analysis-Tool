Using Python data science tools and IEX Finance Market Data API, I created a tool to analyze portfolio risk.  My source files are Holdings reports generated from the Tamrac Portfolio Reporting software suite.  

These scripts will output a portfolio's correlation and covariance in relation to a given benchmark, the returns of the portfolio and benchmark over a given time period, and the portfolio's Sharpe Ratio and daily Value at Risk (VaR).  There are also functions for finding the returns, covariance, and correlation among individual stock tickers.  Below are historical return graphs for the sample portfolio CSV and the sample statistical ouput.  All calculations are for the previous 5 years of daily returns.

![ReturnComparison](https://user-images.githubusercontent.com/63209956/127754219-07e0c074-42fc-4389-a721-6f15aecf668b.png)
![ReturnDistribution](https://user-images.githubusercontent.com/63209956/127754023-43f87066-133d-486a-81c2-a6893aec5973.png)
![SampleOutput](https://user-images.githubusercontent.com/63209956/127754233-6988dab1-cd4e-4247-a8e9-943966010b0d.png)

This will be a helpful tool to any investor that wants to evaluate the risk/return metrics of a singular or series of investment portfolios.
