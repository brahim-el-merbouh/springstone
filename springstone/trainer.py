from pickle import NONE
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
from sklearn.base import BaseEstimator
#from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error
from utils import prophet_preprocessing, prophet_non_business_days
from data import get_data, create_df_for_prophet, create_train_test
from params import PROPHET_COLUMN,PROPHET_PERIOD
from prophet import Prophet
import joblib

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

class Trainer():
    def __init__(self, model, X, y, non_business_days=None):
        """
            model: model to train
            X: pandas DataFrame
            y: pandas Series
            non_business_days: non business days for prophet model
        """
        assert isinstance(X, pd.DataFrame)
        if (y is not None):
            assert isinstance(y, pd.Series)
        if (non_business_days is not None):
            assert isinstance(non_business_days, pd.DataFrame)
        self.model = model
        self.pipeline = None
        self.X = X
        self.y = y
        self.non_business_days= non_business_days

    def set_pipeline(self):
        if self.model == "Prophet":
            self.pipeline = self.get_prophet_pipeline()
        
    def get_prophet_pipeline(self):
        pipe_ph = Pipeline([
            ('prophet_preproc', FunctionTransformer(prophet_preprocessing, kw_args={"column": PROPHET_COLUMN})),
            ('prophet_model', ProphetWrapper(self.non_business_days))
        ])
        return pipe_ph

    def get_RNN_pipeline(self):
        pass

    def compute_performance_metric(self, y_true, y_pred):
        if self.model == "Prophet":
            return mean_absolute_error(y_true, y_pred)
    
    def run(self):
        self.set_pipeline()
        self.pipeline.fit(self.X, self.y)
    
    def evaluate(self, X_test, y_test):
        if self.model == "Prophet":
            y_pred = self.pipeline['prophet_model'].prophet.predict(X_test)['yhat']
        else:
            y_pred = self.pipeline.predict(X_test)
        rmse = self.compute_performance_metric(y_test, y_pred)
        return rmse
    
    def save_model_locally(self, ticker, model_type):
        """Save the model into a .joblib format"""
        joblib.dump(self.pipeline, f'model_{model_type}_{ticker}.joblib')

    def predict(self, X):
        if self.model == "Prophet":
            y_pred = self.pipeline['prophet_model'].prophet.predict(X)['yhat']
        else:
            y_pred = self.pipeline.predict(X)
        return y_pred

if __name__ == "__main__":
    # Get and clean data
    ticker = 'AAPL'
    df = get_data(ticker)
    
    df_nbd = prophet_non_business_days(df)
    df_train, df_test = create_train_test(df)
    trainer_prophet = Trainer(model="Prophet",X=df_train, y=None, non_business_days=df_nbd)
    
    df_test_prophet = create_df_for_prophet(df_test)    
    trainer_prophet.run()
    mae = trainer_prophet.evaluate(df_test_prophet[['ds']], df_test_prophet['y'])
    print(f"MAE: {mae}")
    y_pred = trainer_prophet.predict(df_test_prophet[:5][['ds']])
    print(y_pred)
    trainer_prophet.save_model_locally(ticker,'prophet')