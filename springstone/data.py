import yfinance as yfB
import pandas as pd
import numpy as np
import joblib

def get_data(ticker_name,start="2012-02-18",end="2022-02-19"):
    '''returns a DataFrame from yfinance'''
    data = yfB.download(ticker_name, start, end).drop(columns='Adj Close')
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

def create_train_test(data, train_size = 0.8):
    '''creates the test and train dataset'''
    index = round(train_size*data.shape[0])
    data_train = data.iloc[:index]
    data_test = data.iloc[index:]
    return data_train, data_test

def create_df_for_prophet(data):
    '''creates a dataset fit for prophet'''
    data_prophet = data['Close'].copy().reset_index().rename(columns={'Date': 'ds','Close': 'y'})
    return data_prophet

def download_model(ticker, model_type):
    """Downloads a saved model for a ticker and a model_type
       Input:
            ticker: ticker used by the model
            model_type: type of model used such as prohet or RNN
       Ouptut: return a fited model"""
    if model_type == 'prophet':       # download prophet models saved locally
        return joblib.load(f'model_{model_type}_{ticker}.joblib')

def add_missing_days(data):
    """Returns the input dataframe with missing non business days inserted and forward filled.
       Input:
            data: dataframe with a date index
       Output: original dataframe with non business days inserted"""
    X_ = data.copy()

    # Identify non business days in the data dataframe
    non_business_days = get_missing_dates(X_, True)

    # Create a Nan 2D array with as many rows as we have non business days
    an_array = np.full((non_business_days.shape[0], X_.shape[1]), np.nan)

    # Add the non business days to the original data dataframe
    X_ = pd.concat([
        X_,
        pd.DataFrame(an_array, index=non_business_days, columns=X_.columns)
    ])

    # Re-sort the date index of the data dataframe to have continuous dates index
    X_ = X_.sort_index()
    X_.rename_axis(index='Date', inplace=True)

    # The non business days records have the feature columns populated with the Nan value.
    # Fill the non business day records with the last valid observation forward to the next valid one
    X_.fillna(method='ffill', inplace=True)
    return X_

def drop_nan(data):
    """Drops any record in a dataframe that has a NaN value in one of its column
       Input:
            data: dataframe
       Output: the orignal dataframe minus any record with a NaN value"""
    X_ = data.copy()

    # Remove the records with NaN values
    X_.dropna(inplace=True)
    return X_

def subsample_sequence(array, column, length, horizon=1):
    """Returns a tupple containing a random sample of consecutive
       observations of a numpy array and the output of that array
       at horizon.
       Input:
            array: numpy array to extract a sample from
            column: column # in the array that should be used as the y output
            length: how many consecutive observations we want in the sample
            horizon: how many outputs to skip in the future
        Output:
            X: numpy array sample
            y: output for that sample"""
    last_possible = array.shape[0] - length - horizon
    random_start = np.random.randint(0, last_possible)
    X = array[random_start:random_start + length, :]
    y = array[random_start + length + horizon, column]
    return X, y

def get_X_y(array, column, length_of_observations, horizon=1):
    """Returns a tupple containing a list of random samples of consecutive
       observations of a numpy array and their corresponding outputs at horizon.
       Input:
            array: numpy array to extract the samples from
            column: column # in the array that should be used as the y outputs
            length: how many consecutive observations we want in each sample
            horizon: how many outputs to skip in the future
        Output:
            X: list of numpy array samples
            y: numpy array of corresponding outputs for these samples"""
    X, y = [], []
    for length in length_of_observations:
        xi, yi = subsample_sequence(array, column, length, horizon)
        X.append(xi)
        y.append(yi)
    return X, np.array(y)

if __name__ == "__main__":
    df = get_data('TSLA')
    df_prophet = create_df_for_prophet(df)
    df_train, df_test = create_train_test(df_prophet)
    print(df_test.head())
