from sklearn.metrics import mean_absolute_error
from springstone.data import download_model, get_data, create_df_for_prophet, create_train_test
from springstone.prophet_wrapper import ProphetWrapper
import joblib
from tensorflow.keras.models import load_model
import numpy as np

def compute_performance_metric(model_type, y_true, y_pred):
    if model_type == "prophet":
        return mean_absolute_error(y_true, y_pred)

def evaluate_model(ticker, model_type,  X, y_true):
    """Evaluates a saved model for a ticker and a model_type
       Input:
            ticker: ticker used by the model
            model_type: type of model used such as prohet or RNN
            X_test: test data
            y_test: true target for test data
       Ouptut: return a metric value"""

    y_pred = predict_from_model(ticker, model_type,  X)
    rmse = compute_performance_metric(model_type, y_true, y_pred)

    return rmse

def predict_from_model(ticker, model_type, X):
    """Predicts from a saved model for a ticker and a model_type
       Input:
            ticker: ticker used by the model
            model_type: type of model used such as prohet or RNN
            X: data
       Ouptut: return a dataframe with predicted values"""
    if model_type == "prophet":
        model = download_model(ticker, model_type)
        y_pred = model['prophet_model'].prophet.predict(X)['yhat']
    elif model_type == 'rnn':
        print('Predict from model for rnn')
        preprocessor = joblib.load(f'preprocessor_{ticker}.joblib')
        X_preprocessed = preprocessor.transform(X)
        X_preprocessed = X_preprocessed[-14:,:]
        model = load_model(ticker)
        X_preprocessed = np.expand_dims(X_preprocessed, axis=0)
        scaled_close_prediction = model.predict(X_preprocessed)
        fin_scaller_output = np.zeros((1,7))
        fin_scaller_output[0,1] = scaled_close_prediction
        y_pred = preprocessor\
                                    .named_steps['transform']\
                                    .named_transformers_['fin_scaller']\
                                    .inverse_transform(fin_scaller_output)[0,1]
        y_pred = np.array([y_pred])
    return y_pred

if __name__ == "__main__":
    # Get and clean data
    ticker = 'AAPL'
    model_type='prophet'
    df = get_data(ticker)

    df_train, df_test = create_train_test(df)

    df_test_prophet = create_df_for_prophet(df_test)

    mae = evaluate_model(ticker, model_type, df_test_prophet[['ds']], df_test_prophet['y'])
    print(f"MAE: {mae}")
    y_pred = predict_from_model(ticker, model_type, df_test_prophet[:5][['ds']])
    print(y_pred)
