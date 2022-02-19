import pandas as pd

def bollinger_bands(data, column, period, standard_deviations=2):
    """Bollinger Lower, Middle and Upper bands over a specified period
       Input:
           data: dataframe
           column: column name to apply the Bollinger Bands
           period: number of days of the window
           standard_deviations: number of standard deviation for the lower and upper bands from the middle one
       Output: original dataframe with the {column}_bbl, {column}_bbm, {column}_bbu"""
    result = data.copy()
    sma = result[column].rolling(window=period, closed='right').mean()
    band = standard_deviations * result[column].rolling(window=period, closed='right').std()
    result[f'{column}_bbl'] = sma - band
    result[f'{column}_bbm'] = sma
    result[f'{column}_bbu'] = sma + band
    return result

def moving_average(data, column, period):
    """Average price over a specified period
       Input:
           data: dataframe
           column: column name to apply the moving avreage
           period: number of days of the window
       Output: original dataframe with the {column}_ma"""
    result = data.copy()
    result[f'{column}_ma'] = result[column].rolling(window=period, closed='right').mean()
    return result

if __name__ == "__main__":
    from springstone.data import get_data

    df = get_data('TSLA')
    df = bollinger_bands(df, 'Close', 20)
    df = moving_average(df, 'Close', 7)
    print(df.tail(15))
