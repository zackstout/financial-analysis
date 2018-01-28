
# following sentdex (vids 5-8):

import bs4 as bs
import _pickle as pickle
import requests
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import os
import pandas as pd
import pandas_datareader.data as web
import numpy as np

style.use('ggplot')

def save_sp500_tickers():
    # read data from the wikipedia page's table:
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    # .text gives source code text:
    soup = bs.BeautifulSoup(resp.text)
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    # skip row one with headers:
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)
    # creates a file:
    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
    print(tickers)

    return tickers

# save_sp500_tickers()

def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        #r for read, w for write:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)

    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start = dt.datetime(2000, 1, 1)
    end = dt.datetime(2017, 12, 31)

    for ticker in tickers[:200]:
        print(ticker)
        # not entirely sure how this {} is working syntactically, but it passes in the current thing:
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = web.DataReader(ticker, 'yahoo', start, end)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('we have {}'.format(ticker))


# get_data_from_yahoo()

# Odd, i had to run it a few times to get through all 30 without an error, "can't read URL {0}".


# to combine into a df:

def compile_data():
    with open('sp500tickers.pickle', 'rb') as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()

    # we've only grabbed about 70 so far:
    for count,ticker in enumerate(tickers[:66]):
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df.set_index('Date', inplace=True)

        df.rename(columns = {'Adj Close': ticker}, inplace=True)
        df.drop(['Open', 'High', 'Low', "Close", "Volume"], 1, inplace=True)

        # join dfs together into one big file:
        if main_df.empty:
            main_df = df
        else:
            #with outer, we'll get some NaNs, but we'll never lose data.
            main_df = main_df.join(df, how='outer')

        if count % 10 == 0:
            print(count)

    print(main_df.head())
    main_df.to_csv('sp500_joined_closes.csv')

# Needn't call this again, because it already created our csv for us:
# compile_data()

def visualize_data():
    df = pd.read_csv('sp500_joined_closes.csv');
    # good this is working:
    # df['MMM'].plot()
    # plt.show()

    # Awesome, just runs a correlator function for you:
    df_corr = df.corr()
    print(df_corr.head())

    data = df_corr.values
    fig = plt.figure()
    # 1x1, plot number 1; can put commas if you want:
    ax = fig.add_subplot(111)

    # for a heatmap, we have to build it from scratch:
    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)
    # generates legend:
    fig.colorbar(heatmap)
    # "uno momento"
    ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)

    ax.invert_yaxis()
    ax.xaxis.tick_top()

    column_labels = df_corr.columns
    row_labels = df_corr.index

    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)
    plt.xticks(rotation=90)
    heatmap.set_clim(-1,1)
    plt.tight_layout()
    # ah, it works!
    plt.show()


visualize_data()







# xxx
