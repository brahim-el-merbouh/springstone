import yfinance as yfB

def get_data(ticker_name,start="2012-02-18",end="2022-02-19"):
    '''returns a DataFrame from yfinance'''
    data = yfB.download(ticker_name,start,end)
    return data

def create_train_test(data, train_size = 0.8):
    '''create the test and train dataset'''
    index = round(train_size*data.shape[0])
    data_train = data.iloc[:index]
    data_test = data.iloc[index:]
    return data_train, data_test

def create_df_for_prophet(data):
    '''create a dataset fit for prophet'''
    data_prophet = data['Close'].copy().reset_index().rename(columns={'Date': 'ds','Close': 'y'})
    return data_prophet

if __name__ == "__main__":
    df = get_data('TSLA')
    df_prophet = create_df_for_prophet(df)
    df_train, df_test = create_train_test(df_prophet)
    print(df_test.head())
