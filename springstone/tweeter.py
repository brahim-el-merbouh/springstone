import flair
import re
import pandas as pd
import requests
import tweepy
from springstone import params

sentiment_model = flair.models.TextClassifier.load('en-sentiment')

# add params.bear.....for all of the 5 first
client = tweepy.Client(bearer_token=params.BEARER_TOKEN,
                       consumer_key=params.CONSUMER_KEY,
                       consumer_secret=params.CONSUMER_SECRET,
                       access_token=params.ACCESS_TOKEN,
                       access_token_secret=params.ACCESS_TOKEN_SECRET,
                       return_type=requests.Response,
                       wait_on_rate_limit=True)


#preprocessing text file to prepare for flair analysis
def clean(raw):
    """ Remove hyperlinks and markup """
    result = re.sub("<[a][^>]*>(.+?)</[a]>", 'Link.', raw)
    result = re.sub('&gt;', "", result)
    result = re.sub('&#x27;', "'", result)
    result = re.sub('&quot;', '"', result)
    result = re.sub('&#x2F;', ' ', result)
    result = re.sub('<p>', ' ', result)
    result = re.sub('</i>', '', result)
    result = re.sub('&#62;', '', result)
    result = re.sub('<i>', ' ', result)
    result = re.sub("\n", '', result)
    result = re.sub("(?i)@[a-z0-9_]", '', result)
    result = re.sub("\s+", '', result)
    return result


def tweet_to_sentiment(tweets):
    # Save data as dictionary
    tweets_dict = tweets.json()
    if tweets_dict['meta']['result_count'] > 0:

        # Extract "data" value from dictionary
        tweets_data = tweets_dict['data']
        # Transform to pandas Dataframe
        df = pd.json_normalize(tweets_data)
        df = df.drop(columns=[
            'public_metrics.retweet_count', 'public_metrics.reply_count',
            'public_metrics.quote_count'
        ])
        # we will append probability and sentiment preds later
        probs = []
        sentiments = []

        # use regex expressions (in clean function) to clean tweets
        df['text'] = df['text'].apply(clean)

        for tweet in df['text'].to_list():
            # make prediction
            sentence = flair.data.Sentence(tweet)
            sentiment_model.predict(sentence)
            # extract sentiment prediction
            probs.append(sentence.labels[0].score)  # numerical score 0-1
            sentiments.append(
                sentence.labels[0].value)  # 'POSITIVE' or 'NEGATIVE'

    # add probability and sentiment predictions to tweets dataframe
        df['probability'] = probs
        df['sentiment'] = sentiments

        #ponderate the weight of each tweet
        df['sentiment_direction'] = df['sentiment'].apply(
            lambda x: -1 if x == "NEGATIVE" else 1)
        df['ponderated_value'] = df['public_metrics.like_count'] * df[
            'probability'] * df['sentiment_direction']
        total = df['ponderated_value'].sum(
        ) / df['public_metrics.like_count'].sum()
        return total
    else:
        return 0

# Define query
# copy into params.py
# place the dict into params

def ticker_to_tweets(ticker):
    value = params.TICKER_KEYWORDS[ticker]
    query = f"{value}(from:aswathdamodaran OR from:ukarlewitz OR from:alphatrends OR from:Investor666 OR\
  from:markminervini OR from:TradersCorner OR from:Option_snipper OR from:LMT978 OR from:OptionsHawk OR\
  from:SunriseTrader OR from:traderstewie OR from:IncredibleTrade OR from:CNBC OR from:Benzinga OR\
  from:Stocktwits OR from:BreakoutStocks OR from:bespokeinvest OR from:WSJmarkets OR from:Stephanie_Link OR\
  from:nytimesbusiness OR from:IBDinvestors OR from:WSJDealJournal) - is: retweet"

    tweets = client.search_recent_tweets(
        query=query,
        tweet_fields=['author_id', 'created_at', 'public_metrics'])
    if tweets.status_code == 200:
        score = tweet_to_sentiment(tweets)
        return score
    else:
        return 0

if __name__ == "__main__":
    ticker = 'BAC'
    print(ticker_to_tweets(ticker))
