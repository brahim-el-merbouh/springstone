import pandas as pd

def bollinger_bands(data, column, period, standard_deviations=2, new_columns_only=False):
    """Create a Bollinger band over a specified period.
       Input:
           data: dataframe.
           column: column name to apply the Bollinger Band.
           period: number of days of the window.
           standard_deviations: number of standard deviations. 0 for the middle band, positive number for a upper band,
                                negative number for a lower band.
           new_columns_only: True to return only the Bollinger band column.
                             False to return the original dataframe with the new Bollinger band column.
       Output: a dataframe with the {column}_bb{period}_{standard_deviations}"""
    result = data.copy()
    sma = result[column].rolling(window=period, closed='right').mean()
    band = standard_deviations * result[column].rolling(window=period, closed='right').std()
    new_column_name = f'{column}_bb{int(period)}_{standard_deviations}'
    result[new_column_name] = sma + band
    if new_columns_only:
        return result[[new_column_name]]
    return result

def moving_average(data, column, period, new_columns_only=False):
    """Average price over a specified period.
       Input:
           data: dataframe.
           column: column name to apply the moving avreage.
           period: number of days of the window.
           new_columns_only: True to return only the moving average column.
                             False to return the original dataframe with the new moving average column.
       Output: a dataframe with the {column}_ma{period}"""
    new_column_name = f'{column}_ma{int(period)}'
    result = data.copy()
    result[new_column_name] = result[column].rolling(window=period, closed='right').mean()
    if new_columns_only:
        return result[[new_column_name]]
    return result

def daily_return(data, column):
    """Percentage change in the closing price from today and previous day
       Input:
            data: dataframe
            column: column name to apply to the daily return
       Output: original dataframe with the percentage return column"""
    new_column_name = "percentage_change"
    result = data.copy()
    result[new_column_name] = result[column].pct_change()
    return result

def temp_data_predict(ticker, y_predict):
    """bollinger bands and moving average calculated for the next day predicted y
       Input:
            data: ticker and y_predict
            column: none
       Output: list of values y_predict, bollinger band_predict(20days, 2SD),bollinger band_predict(20days,-2SD) and moving average_predict(7days)"""
    hist = get_data(ticker)
    hist_predict = hist[-40:]
    hist_predict.loc['predict'] = [0, 0, 0, y_predict, 0]
    hist_predict = bollinger_bands(hist_predict, 'Close', 20, 2)
    hist_predict = bollinger_bands(hist_predict, 'Close', 20, -2)
    hist_predict = moving_average(hist_predict, 'Close', 7)
    list_temp = hist_predict[-1:].values
    list_temp = list_temp[0][3:8].tolist()
    list_temp.remove(0.0)
    return list_temp


# Baseline strategy implemented for the recommendation
def basic_recommendation(ticker, y_predict):
    """recommendation for the next day predicted y, 5 options possible
       Input:
            data: ticker and y_predict
            column: none
       Output: one string text that give the recommendation"""
    list_temp = temp_data_predict(ticker, y_predict)
    if y_predict > list_temp[1]:
        if y_predict < list_temp[3]:
            return "Strong sell recommendation"
        else:
            return "Sell recommendation"
    if y_predict < list_temp[2]:
        if y_predict > list_temp[3]:
            return "Strong buy recommendation"
        else:
            return "Buy recommendation"
    else:
        return "Hold"


if __name__ == "__main__":
    from springstone.data import get_data

    df = get_data('TSLA')
    df = bollinger_bands(df, 'Close', 20)
    df = moving_average(df, 'Close', 7)
    print(df.tail(15))
