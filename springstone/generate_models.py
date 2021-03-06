import pandas as pd
from springstone.data import create_df_for_prophet, create_train_test, get_data
from springstone.params import MODEL_TYPE, TICKERS, PROPHET_COLUMN
from springstone.utils import prophet_non_business_days, prophet_preprocessing
from springstone.trainer import Trainer
from springstone.predict import evaluate_model
from springstone.prophet_wrapper import ProphetWrapper

def generate_prophet_models():

    metrics = {'model':[],'MAE':[]}

    for ticker in TICKERS:
        df = get_data(ticker,end='2022-03-12')
        df_nbd = prophet_non_business_days(df)
        df_train, df_test = create_train_test(df)
        trainer_prophet = Trainer(model="prophet",X=df_train, y=None, non_business_days=df_nbd)

        df_test_prophet = prophet_preprocessing(df_test, PROPHET_COLUMN)
        trainer_prophet.run()
        trainer_prophet.save_model_locally(ticker, MODEL_TYPE)
        mape = evaluate_model(ticker, MODEL_TYPE, df_test_prophet[['ds']], df_test_prophet['y'])
        metrics['model'].append(f'{MODEL_TYPE}_{ticker}')
        metrics['MAE'].append(mape)
        pd.DataFrame.from_dict(metrics).to_csv(f'{MODEL_TYPE}_models_metrics.csv', index=False)
        print(metrics)

if __name__ == "__main__":
    generate_prophet_models()
