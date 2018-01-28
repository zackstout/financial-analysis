
# following codedex:
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
# don't forget to pip3 install this as well:
import pandas_datareader.data as web

style.use('ggplot')

# start = dt.datetime(2000, 1, 1)
# end = dt.datetime(2016, 12, 31)
#
# # a dataframe is similar to a spreadsheet:
# df = web.DataReader('TSLA', "yahoo", start, end)
# # generate a csv:
# df.to_csv('tsla.csv')

# # print first 6:
# print(df.head(6))
# # print last 6:
# print(df.tail(6))

# to read information (can also read from a DB, json, etc.):
df = pd.read_csv('tsla.csv', parse_dates = True, index_col = 0)
# print(df.head())

# print(df[['Open', 'High']].head())
#
# df['Adj Close'].plot()
# plt.show()

# Moving average:
df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()
# Get rid of first 100 rows without altering original df. Can use min_periods instead:
# df.dropna(inplace = True)
print(df.head())

# notes that it's weird to refer to subplots as 'axes':
ax1 = plt.subplot2grid( (6, 1), (0, 0), rowspan=5, colspan=1)
# 'share' means zooming on one will also zoom the other one.
ax2 = plt.subplot2grid( (6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)

ax1.plot(df.index, df['Adj Close'])
ax1.plot(df.index, df['100ma'])
ax2.bar(df.index, df['Volume'])
plt.show()
