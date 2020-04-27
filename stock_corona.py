import requests as reqs
import pandas as pd
import matplotlib.pyplot as plt

# a function to retrive .csv from Yahoo
# return a pd dataframe with COP and date
def getCSV(abbr, write_csv):
    abbr = abbr.upper()
    output_filename = abbr+'.csv'
    #make it TODAY
    url = 'https://query1.finance.yahoo.com/v7/finance/download/' + abbr + \
          '?period1=1577836800&period2=1587945431&interval=1d&events=history'
    df = pd.read_csv(url)
    df[abbr] = round((df['Close'] - df['Open']) * 100 / df['Open'], 4)
    df['date'] = df['Date'].astype(str).str[5:]
    output = df[['date', abbr]]
    if write_csv:
        df.to_csv(output_filename, index=False)
    return(output)


# merge multiple data frame into one


# plot a line graph
def plot(stock):
    stock.plot(kind='line', x='date', ax=plt.gca())
    plt.show()


stock = getCSV('STZ', False)
plot(stock)