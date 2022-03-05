from sklearn.base import BaseEstimator
from prophet import Prophet

class ProphetWrapper(BaseEstimator):
    def __init__(self, non_business_days):
        super().__init__()
        self.non_business_days = non_business_days
        self.prophet = Prophet(holidays=self.non_business_days)

    def fit(self, X, y=0):
        self.prophet.fit(X)
        return self
    
    def transform(self, X, y=None):
        pass