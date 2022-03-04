from sklearn.metrics import mean_absolute_error
from data import download_model, get_data, create_df_for_prophet, create_train_test
import trainer
#from trainer import ProphetWrapper

def compute_performance_metric(model_type, y_true, y_pred):
    if model_type == "prophet":
        return mean_absolute_error(y_true, y_pred)

def evaluate(ticker, model_type,  X, y_true):
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
    model = download_model(ticker, model_type)
    if model_type == "prophet":
        y_pred = model['prophet_model'].prophet.predict(X)['yhat']
    else:
        y_pred = model.predict(X)
        
    return y_pred

if __name__ == "__main__":
    # Get and clean data
    ticker = 'AAPL'
    model_type='prophet'
    df = get_data(ticker)
    
    df_train, df_test = create_train_test(df)

    df_test_prophet = create_df_for_prophet(df_test)    
    
    mae = evaluate(ticker, model_type, df_test_prophet[['ds']], df_test_prophet['y'])
    print(f"MAE: {mae}")
    y_pred = predict_from_model(ticker, model_type, df_test_prophet[:5][['ds']])
    print(y_pred)
