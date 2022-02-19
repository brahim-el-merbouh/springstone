from webbrowser import get
import yfinance as yfB
import pandas as pd
import numpy as np

def get_data(ticker_name,start="2012-02-18",end="2022-02-19"):
    '''returns a DataFrame from yfinance'''
    data = yfB.download(ticker_name,start,end)
    return data

def get_missing_dates(dataframe, include_weekends=False):
    """Returns missing dates in the finance data
       Input:
           data: dataframe
       Output: numpy array of dates"""
    start_date = dataframe.index[0]
    end_date = dataframe.index[dataframe.shape[0]-1]
    if include_weekends:
        return np.array(pd.date_range(start = start_date, end = end_date ).difference(dataframe.index))
    else:
        return np.array(pd.bdate_range(start = start_date, end = end_date ).difference(dataframe.index))
