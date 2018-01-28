
# # following sentdex:
# import datetime as dt
# import matplotlib.pyplot as plt
# from matplotlib import style
# from matplotlib.finance import candlestick_ohlc
# # matplotlib uses its own dating system.
# import matplotlib.dates as mdates
#
# import pandas as pd
# # don't forget to pip3 install this as well:
# import pandas_datareader.data as web
#
# style.use('ggplot')
#
# df = pd.read_csv('tsla.csv', parse_dates = True, index_col = 0)
#
# df_ohlc = df['Adj Close'].resample('10D').ohlc()
# df_volume = df['Volume'].resample('10D').sum()
#
# df_ohlc.reset_index(inplace = True)
# df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

import bs4 as bs
import _pickle as pickle
import requests
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web

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

    for ticker in tickers[:30]:
        print(ticker)
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = web.DataReader(ticker, 'yahoo', start, end)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('we have {}'.format(ticker))


get_data_from_yahoo()

# Odd, i had to run it a few times to get through all 30 without an error, "can't read URL {0}".









# xxx
