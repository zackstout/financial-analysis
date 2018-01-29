
# following sentdex vids 9-12:
# we must 'preprocess' the data before we feed it to a machine learning algorithm:

from collections import Counter

import numpy as np
import pandas as pd
# needed for python3, methinks:
import _pickle as pickle

# for machine learning:
from sklearn import svm, cross_validation, neighbors
from sklearn.ensemble import VotingClassifier, RandomForestClassifier

# the question: if we take into account all other companies at every interval, will that give us a better prediction for a single company's future?
# store as buy, sell, or hold:


# Part 9:
def process_data_for_labels(ticker):
    # we care about the week:
    hm_days = 7
    df = pd.read_csv('sp500_joined_closes.csv', index_col=0)
    # maybe we don't need .tolist():
    tickers = df.columns.values.tolist()
    df.fillna(0, inplace=True)

    for i in range(1, hm_days+1):
        # oh i think i see now, the args get passed as values to {}:
        # gets future data. New minus the old.:
        df['{}_{}d'.format(ticker, i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker]

    df.fillna(0, inplace=True)
    return tickers, df

# good, this works (well at least it throws no errors):
# he notes that you want to look at 1 or 2 year past data to get accurate vision of companies' correlation with each other. But will need more than 1-day data.
# process_data_for_labels('ABBV')



# Part 10:
# will only generate a slight edge over random:
# passing *args lets us pass any number of arguments:
def buy_sell_hold(*args):
    cols = [c for c in args]
    requirement = 0.02
    for col in cols:
        if col > requirement:
            return 1
        if col < -requirement:
            return -1
    return 0



# Part 11:
# he struggles to iterate this list, vid 11, "this is so gross, i thought we were past this heresy":
def extract_featuresets(ticker):
    tickers, df = process_data_for_labels(ticker)

    df['{}_target'.format(ticker)] = list(map( buy_sell_hold,
                                    df['{}_1d'.format(ticker)],
                                    df['{}_2d'.format(ticker)],
                                    df['{}_3d'.format(ticker)],
                                    df['{}_4d'.format(ticker)],
                                    df['{}_5d'.format(ticker)],
                                    df['{}_6d'.format(ticker)],
                                    df['{}_7d'.format(ticker)],
                                    ))
# "i'll take a shower after this", lol
# really don' forget its curly braces for variables, not parentheses:
    vals = df['{}_target'.format(ticker)].values.tolist()
    str_vals = [str(i) for i in vals]
    print('data spread:', Counter(str_vals))

    df.fillna(0, inplace=True)
    # to handle dividing by zero:
    df = df.replace([np.inf, -np.inf], np.nan)
    df.dropna(inplace=True)

    # pct_change normalizes for us:
    df_vals = df[[ticker for ticker in tickers]].pct_change()
    df_vals = df_vals.replace([np.inf, -np.inf], 0)
    # error catching:
    df_vals.fillna(0, inplace=True)

    # feature sets and labels:
    X = df_vals.values
    y = df['{}_target'.format(ticker)].values

    # we are ready to machine learn!f
    return X, y, df

# ah yes all we needed was to change all parentheses to braces:
# extract_featuresets('ABBV')



# Part 12:
def do_ml(ticker):
    X, y, df = extract_featuresets(ticker)

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size = 0.25)

    # class fire:
    # clf = neighbors.KNeighborsClassifier()
    # changing this:
    clf = VotingClassifier([('lsvc', svm.LinearSVC()),
                            ('knn', neighbors.KNeighborsClassifier()),
                            ('rfor', RandomForestClassifier())])

    # y_train is 0, -1, or 1:
    clf.fit(X_train, y_train)
    confidence = clf.score(X_test, y_test)
    print('acc: ', confidence)

    predictions = clf.predict(X_test)

    print('predictions:', Counter(predictions))

    return confidence

# hmm, we're getting like 70% accuracy when he says we'd be lucky to get above 35%...:
do_ml('ABBV')







# bye
