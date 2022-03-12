from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from springstone.utils import basic_recommendation, enhanced_recommendation
from springstone.tweeter import ticker_to_tweets

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
@app.get("/")
def index():
    return {"greeting": "Hello world"}

@app.get("/predict")
def predict(ticker):
    recommendation = basic_recommendation(ticker)
    return {'recommendation':recommendation}


@app.get("/predict_enhanced")
def predict_enhanced(ticker):
    recommendation = enhanced_recommendation(ticker)
    return {'recommendation': recommendation}

@app.get("/sentiment")
def sentiment(ticker):
    sentiment= ticker_to_tweets(ticker)
    return {'score': sentiment}
