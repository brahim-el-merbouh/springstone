import pandas as pd
from data import create_df_for_prophet, create_train_test, get_data
from params import MODEL_TYPE, TICKERS
from utils import prophet_non_business_days
from trainer import Trainer
from springstone.predict import evaluate
from springstone.prophet_wrapper import ProphetWrapper

def generate_prophet_models():

    metrics = {'model':[],'MAE':[]}

    for ticker in TICKERS:
        df = get_data(ticker,end='2022-03-04')
        df_nbd = prophet_non_business_days(df)
        df_train, df_test = create_train_test(df)
        trainer_prophet = Trainer(model="prophet",X=df_train, y=None, non_business_days=df_nbd)
        
        df_test_prophet = create_df_for_prophet(df_test)    
        trainer_prophet.run()
        trainer_prophet.save_model_locally(ticker, MODEL_TYPE)
        mae = evaluate(ticker, MODEL_TYPE, df_test_prophet[['ds']], df_test_prophet['y'])
        metrics['model'].append(f'{MODEL_TYPE}_{ticker}')
        metrics['MAE'].append(mae)
        print(metrics)

if __name__ == "__main__":
    generate_prophet_models()