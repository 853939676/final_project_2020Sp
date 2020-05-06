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

    >>> getstock('STZ', False, 'before') # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
          date         STZ   STZ_POC
    0    05-31  176.449997       NaN
    1    06-03  177.229996  0.779999
    2    06-04  184.440002  7.210006
    ...
    146  12-27  189.229996 -0.430008
    147  12-30  188.369995 -0.860001

    [148 rows x 3 columns]

    >>> getstock('STZ', False, 'after') # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
         date         STZ   STZ_POC
    0   01-21  190.229996       NaN
    1   01-22  191.940002  1.710006
    2   01-23  193.970001  2.029999
    ...
    69  04-29  169.419998  1.990005
    70  04-30  164.690002 -4.729996

    [71 rows x 3 columns]

    >>> getstock('BUD', False, 'after') # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
         date        BUD   BUD_POC
    0   01-21  78.809998       NaN
    1   01-22  78.110001 -0.699997
    2   01-23  78.260002  0.150001
    ...
    69  04-29  48.660000  1.810002
    70  04-30  46.520000 -2.140000

    [71 rows x 3 columns]
    """
    abbr = abbr.upper()
    output_filename = abbr+'.csv'
    poc_name = abbr+'_POC'
    if time=='before':
        url = 'https://query1.finance.yahoo.com/v7/finance/download/' + abbr + \
          '?period1=1569024000&period2=1578009600&interval=1d&events=history'
    else:
        url = 'https://query1.finance.yahoo.com/v7/finance/download/' + abbr + \
          '?period1=1579564800&period2=1588283265&interval=1d&events=history'
    #  read the url into dataframe
    df = pd.read_csv(url)
    #  trim the year in Date column
    df['Date'] = df['Date'].astype(str).str[5:]
    df[poc_name] = df['Close'].diff()
    output = df[['Date', 'Close', poc_name]]
    #  rename columns for further steps
    output.columns = ['date', abbr, poc_name]
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

    >>> getCOVID('us', False) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
          date    cases    new
    0    01-21        1      1
    1    01-22        1      0
    2    01-23        1      0
    3    01-24        2      1
    4    01-25        3      1
    ...
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
    area_out.columns = ['date', 'cumulative', 'new']
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

    >>> stz = getstock('STZ', False, 'after')
    >>> bud = getstock('BUD', False, 'after')
    >>> us = getCOVID('us', False)
    >>> stock_covid(stz, bud, us)# doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
         date         STZ   STZ_POC        BUD   BUD_POC      diff    cases    new
    0   01-21  190.229996       NaN  78.809998       NaN       NaN        1      1
    1   01-22  191.940002  1.710006  78.110001 -0.699997 -2.410003        1      0
    2   01-23  193.970001  2.029999  78.260002  0.150001 -1.879998        1      0
    3   01-24  191.559998 -2.410003  77.739998 -0.520004  1.889999        2      1
    4   01-27  190.899994 -0.660004  75.580002 -2.159996 -1.499992        5      0
    ...

    [71 rows x 8 columns]
    """
    output = stz.merge(compare, on='date', how='left')
    output['price_diff'] = output[output.columns[3]] - output[output.columns[1]]
    output['poc_diff'] = output[output.columns[4]] - output[output.columns[2]]
    output = output.merge(covid, on='date', how='left')
    return output


def plot_stock(df):
    """
    This function can plot the stock prices of two different companies and the difference between them

    :param df: the dataframe containing stock prices of two companies
    :return: two graph including a price graph and a difference graph
    """
    fig,ax = plt.subplots(3)
    stz, = ax[0].plot(df['date'],df[df.columns[1]])
    stz.set_label(df.columns[1])
    other, = ax[0].plot(df['date'],df[df.columns[3]])
    other.set_label(df.columns[3])
    ax[0].xaxis.set_major_locator(plt.MaxNLocator(10))
    ax[0].legend()
    stz, = ax[1].plot(df['date'],df[df.columns[2]])
    stz.set_label(df.columns[2])
    other, = ax[1].plot(df['date'],df[df.columns[4]])
    other.set_label(df.columns[4])
    ax[1].xaxis.set_major_locator(plt.MaxNLocator(10))
    ax[1].legend()
    diffP, = ax[2].plot(df['date'],df['price_diff'])
    ax2 = ax[2].twinx()
    diffC, = ax2.plot(df['date'], df['poc_diff'], color='orange')
    ax[2].xaxis.set_major_locator(plt.MaxNLocator(10))
    ax2.legend((diffC, diffP),('price_diff', 'poc_diff'))
    plt.show()


def plot_covid(df, covid):
    """
    This function can plot the stock price differences and covid-19 counts.
    Users can choose to plot either new cases or cumulative confirmed cases.

    :param df: the dataframe containing stock and covid info
    :param covid: cases refers to cumulative confirmed cases
                new refers to new confirmed cases on that day
    :return: a single line graph with two lines
    """
    fig,ax=plt.subplots(2)
    stockP, = ax[0].plot(df['date'], df['price_diff'])
    ax2 = ax[0].twinx()
    cases, = ax2.plot(df['date'], df[covid], color='orange')
    ax[0].xaxis.set_major_locator(plt.MaxNLocator(10))
    ax2.legend((stockP, cases), ('price_diff', covid))

    stockC, = ax[1].plot(df['date'], df['poc_diff'])
    ax3 = ax[1].twinx()
    cases, = ax3.plot(df['date'], df[covid], color='orange')
    ax[1].xaxis.set_major_locator(plt.MaxNLocator(10))
    ax3.legend((stockC, cases), ('poc_diff', covid))
    plt.show()

if __name__ == '__main__':
    #  get covid data of areas that we interested in
    us_covid = getCOVID('us', False)

    #  analyze the stock price difference of Corona Beer with other Beer companies(BUD and TAP)
    BUD_stock_before = stock_covid(getstock('STZ', False, 'before'), getstock('BUD', False, 'before'), us_covid)
    BUD_stock_after = stock_covid(getstock('STZ', False, 'after'), getstock('BUD', False, 'after'), us_covid)
    TAP_stock_before = stock_covid(getstock('STZ', False, 'before'), getstock('TAP', False, 'before'), us_covid)
    TAP_stock_after = stock_covid(getstock('STZ', False, 'after'), getstock('TAP', False, 'after'), us_covid)
    print(BUD_stock_after)
    #  plot stock price differences before and after COVID-19
    plot_stock(BUD_stock_before)
    plot_stock(TAP_stock_before)
    plot_stock(BUD_stock_after)
    plot_stock(TAP_stock_after)

    #  combine stock price difference with daily confirmed COVID-19 cases in the US
    plot_covid(BUD_stock_after, 'cumulative')
    plot_covid(TAP_stock_after, 'cumulative')

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
