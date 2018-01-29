
# we must 'preprocess' the data before we feed it to a machine learning algorithm:
import numpy as np
import pandas as pd
# needed for python3, methinks:
import _pickle as pickle

# the question: if we take into account all other companies at every interval, will that give us a better prediction for a single company's future?

# store as buy, sell, or hold:

def process_data_for_labels(ticker):
    hm_days = 7
    df = pd.read_csv('sp500_joined_closes.csv', index_col=0)
    # maybe we don't need .tolist():
    tickers = df.columns.values.tolist()
    df.fillna(0, inplace=True)

    for i in range(1, hm_days+1):
        # oh i think i see now, the args get passed as values to {}:
        # gets future data:
        df['{}_{}d'.format(ticker, i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker]

    df.fillna(0, inplace=True)
    return tickers, df

process_data_for_labels('MMM')
