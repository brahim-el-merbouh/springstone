from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class MovingAverageTransformer(BaseEstimator, TransformerMixin):
    """
        Computes the Average price over a specified period or a given column
        Returns a copy of the DataFrame X with only one column: {column}_ma.
    """
    def __init__(self, column,period):
        self.column = column
        self.period = period

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        assert isinstance(X, pd.DataFrame)
        X_ = X.copy()
