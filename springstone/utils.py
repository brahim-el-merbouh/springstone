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

if __name__ == "__main__":
    from springstone.data import get_data

    df = get_data('TSLA')
    df = bollinger_bands(df, 'Close', 20)
    df = moving_average(df, 'Close', 7)
    print(df.tail(15))
