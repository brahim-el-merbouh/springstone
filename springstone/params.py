BOLLINGER_PERIOD = 7
MOVING_AVERAGE_PERIOD = 7
BOLLINGER_COLUMN = 'Close'
MOVING_AVERAGE_COLUMN = 'Close'
BOLIINGER_SD = 2
PROPHET_COLUMN = 'Close'
PROPHET_PERIOD = 7
MODEL_TYPE = 'rnn'
TICKERS = ['AAPL', 'TSLA', 'AMZN', 'BTC-USD', 'SPY','RIOT']
BUCKET_NAME = 'wagon-data-716-el-merbouh'
TRAINING_DIRECTORY = 'trainings'

# credentials for tweeter.api
CONSUMER_KEY = "HN4HDYwIzatkeVMftVdpNq1b5"
CONSUMER_SECRET = "6RWcc6qyBh5hu6XhLpgpb5HjmyjKOElpR5l7a5K7XNy5ffYR3P"
ACCESS_TOKEN = "745868496848953344-OJMeny3ow43jGAToTUzdcTprknfN87p"
ACCESS_TOKEN_SECRET = "kH6t5Az7t2QAWWT5MoTSY5vFMmBWo6KRQlFDucN7XYQWH"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAALqAYQEAAAAAu9eBut5eSqcDtAtnpjaK4bBPInU%3DZ5dG7iBEDwII7Nj3QxSKqsZhb4Fpm6qmBngnuStTrMQeYMQUNE"

# from ticker to keywords for the  tweeter.api query
TICKER_KEYWORDS = {
    "TSLA": "(TSLA OR Elon Musk OR TESLA)",
    "AAPL": "(AAPL OR Apple)",
    "BTC-USD": "(BTC-USD OR Bitcoin)",
    "SPY": "(SPY OR S&P 500 OR S&P-500)",
    "RIOT": "(RIOT)",
    "AMZN": "(AMZN OR Jeff Bezos OR AMAZON)",
    "BAC": "(Bank of America OR BAC OR BoA)",
    "FB": "(facebook OR FB OR Meta OR Zuckerberg)",
    "ROSN": "(Rosneft OR ROSN)",
    "NVTK": "(NVTK OR Novatek)"
}

THRESHOLD = 0.75
