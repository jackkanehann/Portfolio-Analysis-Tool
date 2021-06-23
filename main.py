import pandas as pd
import get_csv_module

currentPortfolio = get_csv_module.CSVGetInfo("/Users/jackk/Projects/pythonProjects/PortfolioAnalysis/", "holdings_sample.csv")

get_csv_module.display_file_location(currentPortfolio.path, currentPortfolio.file_name)

##show inital columns in csv
currentPortfolio.display_summary()

##create dataframe with preprocessed csv data
portfolio_df = pd.read_csv(currentPortfolio.path + currentPortfolio.file_name)
portfolio_df = portfolio_df.drop(['Data For', 'Managed?', 'Accrued Income'], axis=1)
portfolio_df.drop_duplicates(subset='Symbol', keep=False, inplace=True, ignore_index=False)
print(portfolio_df.head(99))

##rearrange and add columns
print(list(portfolio_df.columns))
portfolio_df.insert(1,'Weight',0)
print(list(portfolio_df.columns))

newColumns = ['Symbol', 'Quantity','Price','Value','Weight','As of Date']
portfolio_df = portfolio_df[newColumns]
print(list(portfolio_df.columns))


##convert csv data into portfolio dataframe
##create portfolio dataframe from input instead of csv import
##run portfolio return correlation to S&P500
##Out portfolio weekly VaR

##As of Date	Data For	Managed?	Symbol	Quantity	Value	Price	Accrued Income


##Codes inside the if statement below runs only when the script is being run as a standalone script.
##if __name__ == '__main__':
##What about for __init__:?



