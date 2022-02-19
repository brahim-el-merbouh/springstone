import yfinance as yfB
def get_data(ticker_name,start="2012-02-18",end="2022-02-19"):
    '''returns a DataFrame from yfinance'''
    data = yfB.download(ticker_name,start,end)
    return data
