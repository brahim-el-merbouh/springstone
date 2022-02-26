import pandas as pd
import numpy as np
from springstone.data import get_missing_dates, create_df_for_prophet

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

def prophet_preprocessing(data, column):
    """Convert a ticker dataframe into a Prophet compatible dataframe [['ds', 'y']]
       where y is the column feature/output we want to keep from the ticker dataframe
       and where missing non business days are included too and forward filled
       Input:
            data: dataframe with a date index and at least 1 feature column
            column: column name to use as the y Prophet feature/output
       Output: dataframe in Prophet format incuding non business days"""
    # Identify non business days in the data dataframe
    non_business_days = get_missing_dates(data, True)

    # Create a Nan 2D array with as many rows as we have non business days
    an_array = np.full((non_business_days.shape[0], 1), np.nan)

    # Add the non business days to the original data dataframe reduced to the column me want to keep as a feature
    data = pd.concat([data[[column]], pd.DataFrame(an_array, index=non_business_days, columns=[column])])

    # Re-sort the date index of the data dataframe to have continuous dates index
    data = data.sort_index()
    data.rename_axis(index='Date', inplace=True)

    # The non business days records have the feature column populated with the Nan value.
    # Fill the non business day records with the last valid observation forward to the next valid one
    data = data.fillna(method='ffill')

    # Return the data frame formatted in Prophet expected format
    return create_df_for_prophet(data)

def prophet_non_business_days(data):
    """Return a dataframe of non business days in Prophet format
       Input:
            data:dataframe with a data index where missing dates are considered non business days
       Output: dataframe of non business days in Prophet format [['holiday', 'ds']]"""
    return pd.DataFrame({'holiday': 'non business day', 'ds': get_missing_dates(data, True)})


if __name__ == "__main__":
    from springstone.data import get_data

    df = get_data('TSLA')
    df = bollinger_bands(df, 'Close', 20)
    df = moving_average(df, 'Close', 7)
    print(df.tail(15))
