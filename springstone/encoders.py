from sklearn.base import BaseEstimator, TransformerMixin
from utils import moving_average, bollinger_bands
import pandas as pd

class MovingAverageTransformer(BaseEstimator, TransformerMixin):
    """
        Computes the Average price over a specified period or a given column
        Returns a copy of the DataFrame X with only one column: {column}_ma.
    """
    def __init__(self, column='Close',period=7):
        self.column = column
        self.period = period

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        assert isinstance(X, pd.DataFrame)
        X_ = X.copy()
        column_name = f'{self.column}_ma_{str(self.period)}'
        X_[column_name] = moving_average(
            X,
            self.column,
            self.period,
            new_columns_only=True
        )
        return X_[[column_name]]

class BollingerBandsTransformer(BaseEstimator, TransformerMixin):
    """
        Computes the Bollinger band over a specified period
        Returns a copy of the DataFrame X with only one column: {column}_bb_{period}_{standard_deviation}.
    """
    def __init__(self, 
                 column='Close',
                 period=7,
                 standard_deviation=2
                ):
        self.column = column
        self.period = period
        self.standard_deviation = standard_deviation

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        assert isinstance(X, pd.DataFrame)
        X_ = X.copy()
        column_name = f'{self.column}_bb_{str(self.period)}_{str(self.standard_deviation)}'
        X_[column_name] = bollinger_bands(
            X,
            self.column,
            self.period,
            self.standard_deviation,
            new_columns_only=True
        )
        return X_[[column_name]]

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
        return X_[['dow', 'month', 'year']]
