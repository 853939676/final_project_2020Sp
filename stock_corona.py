# Final Project for IS590PR Spring2020
# Rui Liu(ruiliu8)
# GitHub ID: 853939676

import pandas as pd
import matplotlib.pyplot as plt


def getstock(abbr, write_csv, time):
    """
    This function can retrieve a csv containing stock prices of a single company
    from yahoo finance https://finance.yahoo.com/
    and return a cleaned dataframe which contains only date and close price

    :param abbr: abbreviation of company stock name
        abbreviation related to this project:
            ^GSPC for S&P 500
            BUD for Anheuser-Busch InBev SA/NV
            STZ for Constellation Brands, Inc.
    :param write_csv: users can indicate if they want to download the complete .csv to local
                      the file will be named as the stock abbreviation
    :param time: before refers to stock price before the spread of COVID-19(05-31-2019 to 12-31-2019)
                 after refers to stock price after the spread of COVID-19(01-11-2020 to 04-30-2020)
    :return: dataframe contains date(MM-DD) and close price of the day(named with stock abbr)
    """
    abbr = abbr.upper()
    output_filename = abbr+'.csv'
    if time=='before':
        url = 'https://query1.finance.yahoo.com/v7/finance/download/' + abbr + \
          '?period1=1559260800&period2=1577750400&interval=1d&events=history'
    else:
        url = 'https://query1.finance.yahoo.com/v7/finance/download/' + abbr + \
          '?period1=1579564800&period2=1588283265&interval=1d&events=history'
    #  read the url into dataframe
    df = pd.read_csv(url)
    #  trim the year in Date column
    df['Date'] = df['Date'].astype(str).str[5:]
    output = df[['Date', 'Close']]
    #  rename columns for further steps
    output.columns = ['date', abbr]
    if write_csv:
        df.to_csv(output_filename, index=False)
    return(output)


def getCOVID(area_name, write_csv):
    """
    This function can retrieve a csv containing the most update covid-19 data(us and states)
    from github repository https://github.com/nytimes/covid-19-data

    :param area_name: users can specify a state by entering the full name
                      or simply enter 'us' to get the data of the entire country
    :param write_csv: users can indicate if they want to download the complete .csv to local
                      the file will be named as state name(or us)
    :return: dataframe contains date, cumulative cases and new confirmed cases
    """
    if area_name.lower() == 'us':  # url for us data
        url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
        area = pd.read_csv(url)
    else:  # url for state data
        url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
        df = pd.read_csv(url)
        df['state'] = df['state'].str.lower()
        # extract the target state
        area = df[df['state'] == area_name]
        area = area.reset_index()
    # trim date
    area['date'] = area['date'].astype(str).str[5:]
    # calculate new confirmed cases based on cumulative number
    area['new'] = area.cases.diff()
    # manually fill the first row of the data
    area.loc[area.index[0], 'new'] = area.loc[area.index[0], 'cases']
    area['new'] = area['new'].astype('int64')
    if write_csv:
        output_filename = area_name.lower()+'_COVID.csv'
        area = area.drop(columns=['index','state','fips'], axis=1)
        area.to_csv(output_filename, index=False)
    area_out = area[['date', 'cases', 'new']]
    return area_out


def stock_covid(stz, compare, covid):
    """
    This function takes two stock dataframe to calculate the difference between daily stock prices,
    the difference refers to 'how much stz is lower than the other company'.
    Then merged it with the covid dataframe by left join since stock market does not open during weekend
    and we are only keeping covid number for weekdays.

    :param stz: since the project focuses on Corona Beer, its company STZ should always be one input
    :param compare: the other stock price data that users interested in
    :param covid: covid-19 data of the selected area
    :return: a merged dataset with date, two stock prices, differences, covid confirmed and new cases
    """
    output = stz.merge(compare, on='date', how='left')
    output['diff'] = output[output.columns[2]] - output[output.columns[1]]
    output = output.merge(covid, on='date', how='left')
    return output


def plot_stock(df):
    """
    This function can plot the stock prices of two different companies and the difference between them

    :param df: the dataframe containing stock prices of two companies
    :return: two graph including a price graph and a difference graph
    """
    fig,ax = plt.subplots(2)
    stz, = ax[0].plot(df['date'],df[df.columns[1]])
    stz.set_label(df.columns[1])
    other, = ax[0].plot(df['date'],df[df.columns[2]])
    other.set_label(df.columns[2])
    ax[0].xaxis.set_major_locator(plt.MaxNLocator(10))
    ax[0].legend()
    diff, = ax[1].plot(df['date'],df['diff'])
    diff.set_label('diff')
    ax[1].xaxis.set_major_locator(plt.MaxNLocator(10))
    ax[1].legend()
    plt.show()


def plot_covid(df, how):
    """
    This function can plot the stock price differences and covid-19 counts.
    Users can choose to plot either new cases or cumulative confirmed cases.

    :param df: the dataframe containing stock and covid info
    :param how: cases refers to cumulative confirmed cases
                new refers to new confirmed cases on that day
    :return: a single line graph with two lines
    """
    fig,ax=plt.subplots()
    stock, = ax.plot(df['date'], df['diff'])
    stock.set_label('diff')
    ax2 = ax.twinx()
    cases, = ax2.plot(df['date'], df[how], color='orange')
    cases.set_label(how)
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))
    ax.legend()
    ax2.legend()
    plt.show()

if __name__ == '__main__':
    #  get covid data of areas that we interested in
    us_covid = getCOVID('us', False)

    #  analyze the stock price difference of Corona Beer with other Beer companies(BUD and TAP)
    BUD_stock_before = stock_covid(getstock('STZ', False, 'before'), getstock('BUD', False, 'before'), us_covid)
    BUD_stock_after = stock_covid(getstock('STZ', False, 'after'), getstock('BUD', False, 'after'), us_covid)
    TAP_stock_before = stock_covid(getstock('STZ', False, 'before'), getstock('TAP', False, 'before'), us_covid)
    TAP_stock_after = stock_covid(getstock('STZ', False, 'after'), getstock('TAP', False, 'after'), us_covid)

    #  plot stock price differences before and after COVID-19
    plot_stock(BUD_stock_before)
    plot_stock(TAP_stock_before)
    plot_stock(BUD_stock_after)
    plot_stock(TAP_stock_after)

    #  combine stock price difference with daily confirmed COVID-19 cases in the US
    plot_covid(BUD_stock_after, 'new')
    plot_covid(TAP_stock_after,'new')

    #  additional analysis can also be done using this program:
    #  1. compare stock price difference of Corona Beer and S&P 500 number
    GSPC_stock_before = stock_covid(getstock('STZ', False, 'before'), getstock('^GSPC', False, 'before'), us_covid)
    GSPC_stock_after = stock_covid(getstock('STZ', False, 'after'), getstock('^GSPC', False, 'after'), us_covid)
    plot_stock(GSPC_stock_before)
    plot_stock(GSPC_stock_after)
    #  2. compare stock price difference with daily confirmed COVID-19 cases in Illinois state
    illinois_covid = getCOVID('illinois', False)
    BUD_stock_IL = stock_covid(getstock('STZ', False, 'after'), getstock('BUD', False, 'after'), illinois_covid)
    TAP_stock_IL = stock_covid(getstock('STZ', False, 'after'), getstock('TAP', False, 'after'), illinois_covid)
    plot_covid(BUD_stock_IL, 'new')
    plot_covid(TAP_stock_IL, 'new')

    #  From the graph produced above, we can draw three conclusions:
    #  1. The spread of COVID-19 did negatively impacted the stock price of Corona Beer
    #     compared with other beer companies, especially from 3/06 to 3/18.
    #  2. The effect of COVID-19 is decreasing after 3/18.
    #  3. There might be a positive relationship between COVID-19
    #     and the stock price of Corona Beer compared with S&P 500 number.