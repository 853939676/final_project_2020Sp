import requests as reqs
import pandas as pd
import matplotlib.pyplot as plt

# a function to retrive .csv from Yahoo
# return a pd dataframe with COP and date
def getstock(abbr, write_csv):
    abbr = abbr.upper()
    output_filename = abbr+'.csv'
    #make it TODAY
    url = 'https://query1.finance.yahoo.com/v7/finance/download/' + abbr + \
          '?period1=1579564800&period2=1587945431&interval=1d&events=history'
    df = pd.read_csv(url)
    df['ChangeRate'] = round((df['Close'] - df['Open']) * 100 / df['Open'], 4)
    df['Date'] = df['Date'].astype(str).str[5:]
    output = df[['Date', 'ChangeRate']]
    output.columns = ['date', abbr]
    if write_csv:
        df.to_csv(output_filename, index=False)
    return(output)

#get the most up to date COVID info
#generate cumulative stat
def getCOVID(area_name, write_csv):
    if area_name.lower() == 'us':
        url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
        area = pd.read_csv(url)
    else:
        url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
        df = pd.read_csv(url)
        df['state'] = df['state'].str.lower()
        area = df[df['state'] == area_name]
        area = area.reset_index()
    area['date'] = area['date'].astype(str).str[5:]
    area['new'] = area.cases.diff()
    area.loc[area.index[0], 'new'] = area.loc[area.index[0], 'cases']
    area['new'] = area['new'].astype('int64')
    if write_csv:
        output_filename = area_name.lower()+'_COVID.csv'
        area = area.drop(columns=['index','state','fips'], axis=1)
        area.to_csv(output_filename, index=False)
    area_out = area[['date', 'cases', 'new']]
    return area_out


# merge multiple data frame into one


# plot a line graph
def plot(price,covid):
    ax1 = price.plot()
    price.plot(kind='line', x='date', ax=ax1)
    ax2 = ax1.twinx()
    covid.plot(kind='line',x='date', y='new', ax=ax2)
    plt.show()



#list = []
#list.append(getstock('STZ', False))
#list.append(getstock('^GSPC', False))
plot(getstock('STZ', False), getCOVID('illinois', False))