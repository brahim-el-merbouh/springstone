from pickle import NONE
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
#from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error
from utils import prophet_preprocessing
from data import get_data, create_df_for_prophet
from params import PROPHET_COLUMN,PROPHET_PERIOD
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
        pipe_ph = Pipeline([
            ('prophet_preproc', FunctionTransformer(lambda df: prophet_preprocessing(df,PROPHET_COLUMN))),
            ('prophet_model', Prophet(holidays=self.non_business_days))
        ])
    def get_RNN_pipeline(self):
        pass

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

if __name__ == "__main__":
    # Get and clean data
    df = get_data('TSLA')
    df_prophet = clean_data(df)
    y = df["fare_amount"]
    X = df.drop("fare_amount", axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    # Train and save model, locally and
    trainer = Trainer(X=X_train, y=y_train)
    trainer.set_experiment_name('xp2')
    trainer.run()
    rmse = trainer.evaluate(X_test, y_test)
    print(f"rmse: {rmse}")
    trainer.save_model()