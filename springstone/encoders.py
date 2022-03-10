from sklearn.base import BaseEstimator, TransformerMixin
from springstone.utils import moving_average, bollinger_bands, daily_return
import pandas as pd

class MovingAverageTransformer(BaseEstimator, TransformerMixin):
    """
        Computes the Average price over a specified period or a given column
        Returns a copy of the DataFrame X with only one column: {column}_ma.
    """

    def __init__(self, col='Close', period=7, new_columns_only=False):
        self.col = col
        self.period = period
        self.new_columns_only = new_columns_only

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        assert isinstance(X, pd.DataFrame)
        X_ = X.copy()
        return moving_average(X_, self.col, self.period, self.new_columns_only)

class BollingerBandsTransformer(BaseEstimator, TransformerMixin):
    """
        Computes the Bollinger band over a specified period
        Returns a copy of the DataFrame X with only one column: {column}_bb_{period}_{standard_deviation}.
    """
    def __init__(self,
                 col='Close',
                 period=20,
                 standard_deviations=2,
                 new_columns_only=False
                ):
        self.col = col
        self.period = period
        self.standard_deviations = standard_deviations
        self.new_columns_only = new_columns_only

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        assert isinstance(X, pd.DataFrame)
        X_ = X.copy()
        return bollinger_bands(X_, self.col, self.period, self.standard_deviations, self.new_columns_only)


class TimeFeaturesEncoder(BaseEstimator, TransformerMixin):
    """
        Extracts the day of week (dow), the month and the year from a time column.
        Returns a copy of the DataFrame X with only four columns: 'dow', 'month', 'year'.
    """

    def __init__(self):
        pass
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        assert isinstance(X, pd.DataFrame)
        X_ = X.copy()
        X_["dow"] = X_.index.weekday+1
        X_["month"] = X_.index.month
        X_["year"] = X_.index.year
        return X_


class DailyReturnTransformer(BaseEstimator, TransformerMixin):
    """
        Computes the Percentage change of a given column from today and previous day
        Returns a copy of the DataFrame X with only one column: {column}_ma.
    """

    def __init__(self, column='Close', new_columns_only=False):
        self.column = column
        self.new_columns_only = new_columns_only

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        assert isinstance(X, pd.DataFrame)
        X_ = X.copy()
        return daily_return(X_, self.column, self.new_columns_only)
