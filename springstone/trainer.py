from pickle import NONE
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
#from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error
from utils import prophet_preprocessing, prophet_non_business_days
from data import get_data, create_df_for_prophet
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

class Trainer():
    def __init__(self, model, X, y, non_business_days=None):
        """
            model: model to train
            X: pandas DataFrame
            y: pandas Series
            non_business_days: non business days for prophet model
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
        pipe_ph = Pipeline([
            ('prophet_preproc', FunctionTransformer(lambda df: prophet_preprocessing(df,PROPHET_COLUMN))),
            ('prophet_model', ProphetWrapper(self.non_business_days))
        ])
        return pipe_ph

    def get_RNN_pipeline(self):
        pass

    def compute_performance_metric(self, y_true, y_pred):
        if isinstance(self.model, Prophet):
            return mean_absolute_error(y_true, y_pred)
    def run(self):
        self.set_pipeline()
        self.pipeline.fit(self.X, self.y)

    def evaluate(self, X_test, y_test):
        if isinstance(self.model, Prophet):
            y_pred = self.pipeline['prophet_model'].prophet.predict(X_test['ds'])
        else:
            y_pred = self.pipeline.predict(X_test)
        rmse = self.compute_performance_metric(y_test, y_pred)
        return rmse
    
    def save_model_locally(self, ticker, model_type):
        """Save the model into a .joblib format"""
        joblib.dump(self.pipeline, f'model_{model_type}_{ticker}.joblib')

    def predict(self, )

if __name__ == "__main__":
    # Get and clean data
    df = get_data('TSLA')
    #df_prophet = clean_data(df)
    #y = df["Close"]
    #X = df.drop("Close", axis=1)
    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    # Train and save model, locally and
    df_nbd = prophet_non_business_days(df)
    trainer_prophet = Trainer(X=df, y=None, non_business_days=df_nbd)
    #trainer.set_experiment_name('xp2')
    trainer.run()
    rmse = trainer.evaluate(X_test, y_test)
    print(f"rmse: {rmse}")
    trainer.save_model()