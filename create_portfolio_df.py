import pandas as pd
import get_csv_module

print("create_portfolio_df has loaded")

def transformCSV(dataframe):

    ##preprocess data columns
    dataframe = dataframe.drop(['Data For', 'Managed?', 'Accrued Income'], axis=1)
    dataframe.drop_duplicates(subset='Symbol', keep=False, inplace=True, ignore_index=False)
    dataframe.dropna(axis=0, inplace=True)

    ##remove commas for float declarations
    dataframe = dataframe.replace(',','', regex=True)
    dataframe.insert(1,'Weight',0)
    dataframe['Quantity'] = dataframe['Quantity'].astype(float)
    dataframe['Price'] = dataframe['Price'].astype(float)
    dataframe['Value'] = dataframe['Value'].astype(float)
    dataframe['Weight'] = dataframe['Weight'].astype(float)

    dataframe.Weight = dataframe.Value / dataframe['Value'].sum()

    return dataframe

def recalculateWeights(dataframe):

    dataframe.Weight = dataframe.Value / dataframe['Value'].sum()

    return dataframe



