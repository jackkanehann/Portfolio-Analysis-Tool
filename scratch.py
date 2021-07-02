
currentPortfolio = get_csv_module.CSVGetInfo("/Users/jackk/Projects/pythonProjects/PortfolioAnalysis/", "holdings_sample.csv")

get_csv_module.display_file_location(currentPortfolio.path, currentPortfolio.file_name)

##show inital columns in csv
currentPortfolio.display_summary()

##create dataframe with preprocessed csv data
portfolio_df = pd.read_csv(currentPortfolio.path + currentPortfolio.file_name)
portfolio_df = portfolio_df.drop(['Data For', 'Managed?', 'Accrued Income'], axis=1)
portfolio_df.drop_duplicates(subset='Symbol', keep=False, inplace=True, ignore_index=False)
portfolio_df.dropna(axis=0, inplace=True)

##remove commas from dataframe strings
portfolio_df = portfolio_df.replace(',','', regex=True)

print(portfolio_df)

##rearrange and add columns
print(list(portfolio_df.columns))
portfolio_df.insert(1,'Weight',0)
print(list(portfolio_df.columns))

newColumns = ['Symbol', 'Quantity','Price','Value','Weight','As of Date']
portfolio_df = portfolio_df[newColumns]
print(list(portfolio_df.columns))


portfolio_df['Quantity'] = portfolio_df['Quantity'].astype(float)
portfolio_df['Price'] = portfolio_df['Price'].astype(float)
portfolio_df['Value'] = portfolio_df['Value'].astype(float)
portfolio_df['Weight'] = portfolio_df['Weight'].astype(float)
##same for price and value and weight

portfolio_df.Weight = portfolio_df.Value / portfolio_df['Value'].sum()
print(portfolio_df.head(99))
##convert csv data into portfolio dataframe
##create portfolio dataframe from input instead of csv import


currentPortfolio = get_csv_module.CSVGetInfo("/Users/jackk/Projects/pythonProjects/PortfolioAnalysis/", "holdings_sample.csv")

get_csv_module.display_file_location(currentPortfolio.path, currentPortfolio.file_name)

##show inital columns in csv
currentPortfolio.display_summary()

##create dataframe with preprocessed csv data
portfolio_df = pd.read_csv(currentPortfolio.path + currentPortfolio.file_name)
portfolio_df = portfolio_df.drop(['Data For', 'Managed?', 'Accrued Income'], axis=1)
portfolio_df.drop_duplicates(subset='Symbol', keep=False, inplace=True, ignore_index=False)
portfolio_df.dropna(axis=0, inplace=True)

##remove commas from dataframe strings
portfolio_df = portfolio_df.replace(',','', regex=True)

print(portfolio_df)

##rearrange and add columns
print(list(portfolio_df.columns))
portfolio_df.insert(1,'Weight',0)
print(list(portfolio_df.columns))

newColumns = ['Symbol', 'Quantity','Price','Value','Weight','As of Date']
portfolio_df = portfolio_df[newColumns]
print(list(portfolio_df.columns))


portfolio_df['Quantity'] = portfolio_df['Quantity'].astype(float)
portfolio_df['Price'] = portfolio_df['Price'].astype(float)
portfolio_df['Value'] = portfolio_df['Value'].astype(float)
portfolio_df['Weight'] = portfolio_df['Weight'].astype(float)
##same for price and value and weight

portfolio_df.Weight = portfolio_df.Value / portfolio_df['Value'].sum()
print(portfolio_df.head(99))
##convert csv data into portfolio dataframe
##create portfolio dataframe from input instead of csv import
""" """


class Portfolio:
        
    def __init__(self, dataframe):
        self.dataframe = dataframe

