import pandas as pd
from springstone.data import create_train_test, get_data
from springstone.params import TICKERS, PROPHET_COLUMN
from springstone.utils import prophet_preprocessing
from springstone.predict import evaluate_model
import joblib
from tensorflow.keras.models import load_model
from springstone.data import get_data
import numpy as np


def compare_models():

    metrics = {'Ticker': [], 'Prophet MAPE': [], 'RNN MAPE': []}

    for ticker in TICKERS:
        df = get_data(ticker, end='2022-03-12')
        preprocessor = joblib.load(f'preprocessor_{ticker}.joblib')

        df_train, df_test = create_train_test(df)

        df_test_rnn_preprocessed = preprocessor.transform(df_test)

        rnn_model = load_model(ticker)

        df_test_rnn_preprocessed = np.expand_dims(df_test_rnn_preprocessed, axis=0)
        df_test_rnn_preprocessed_stacked = df_test_rnn_preprocessed[:,df_test_rnn_preprocessed.shape[1] - 15:df_test_rnn_preprocessed.shape[1] - 1,:]
        y_test_rnn_preprocessed_stacked = df_test_rnn_preprocessed[0,-1:,1]

        for observation in range(df_test_rnn_preprocessed.shape[1] - 2, 13, -1):
            df_test_rnn_preprocessed_stacked = np.vstack((df_test_rnn_preprocessed[:,observation - 14:observation,:], df_test_rnn_preprocessed_stacked))
            y_test_rnn_preprocessed_stacked = np.append(df_test_rnn_preprocessed[0,observation,1], y_test_rnn_preprocessed_stacked)

        rnn_loss, rnn_mape, rnn_mae = rnn_model.evaluate(df_test_rnn_preprocessed_stacked, y_test_rnn_preprocessed_stacked)

        df_test_prophet = prophet_preprocessing(df_test, PROPHET_COLUMN)[-df_test_rnn_preprocessed_stacked.shape[0]:]

        prophet_mape = evaluate_model(ticker, 'prophet', df_test_prophet[['ds']], df_test_prophet['y'])
        metrics['Ticker'].append(ticker)
        metrics['Prophet MAPE'].append(prophet_mape)
        metrics['RNN MAPE'].append(rnn_mape)
        pd.DataFrame.from_dict(metrics).to_csv('models_metrics.csv', index=False)
        print(metrics)


if __name__ == "__main__":
    compare_models()
