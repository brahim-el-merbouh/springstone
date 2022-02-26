from pickle import NONE
import pandas as pd
from sklearn.pipeline import Pipeline
#from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
#from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error
from prophet import Prophet

class Trainer():
    def __init__(self, model, X, y, non_business_days=None):
        """
            X: pandas DataFrame
            y: pandas Series
        """
        assert isinstance(X, pd.DataFrame)
        assert isinstance(y, pd.Series)
        if (non_business_days is not None):
            assert isinstance(non_business_days, pd.DataFrame)
        self.model = model
        self.pipeline = None
        self.X = X
        self.y = y
        self.non_business_days= self.non_business_days

    def set_pipeline(self):
        if isinstance(self.model, Prophet):
            self.pipeline = self.get_prophet_pipeline()
    def get_prophet_pipeline(self):
        pipe = Pipeline([
            ('prophet_model', Prophet(self.non_business_days))
        ])
    def get_RNN_pipeline(self):
        
    def compute_performance_metric(self, y_true, y_pred):
        if isinstance(self.model, Prophet):
            return mean_absolute_error(y_true, y_pred)
    def run(self):
        self.set_pipeline()
        self.pipeline.fit(self.X, self.y)

    def evaluate(self, X_test, y_test):
        y_pred = self.pipeline.predict(X_test)
        rmse = self.compute_performance_metric(y_test, y_pred)
        return rmse