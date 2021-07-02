import pandas as pd
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


print(portfolio_df.head(10))


##create companion functions in create_portfolio_df.py to transform raw CSV data into workable dataframe
##how to import functions from another module?


##run portfolio return correlation to S&P500
##Out portfolio weekly VaR