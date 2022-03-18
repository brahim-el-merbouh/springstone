from email.policy import default
import streamlit as st
from data import get_data
import pandas as pd
import numpy as np
from plotly import graph_objs as go
import datetime as dt
from datetime import date
from ui_utils import basic_recommendation, moving_average, bollinger_bands
import matplotlib.pyplot as plt
import yfinance as yf
import requests

# -----------Page Layout----------------------

st.set_page_config(layout="wide")
st.title("SpringStone Stock Prediction")

# -----------Date Input------------------------

st.sidebar.write("Please choose the stock symbol and dates:")

today = dt.datetime.today()

start = st.sidebar.date_input('Start date:',
                                   today - dt.timedelta(days=90*1),
                                   min_value=today - dt.timedelta(days=365*10),
                                   max_value=today - dt.timedelta(days=31*2))
end = st.sidebar.date_input('End date:',
                                 min_value=start +
                                 dt.timedelta(days=31*2),
                                 max_value=today)

# -----------Stock Selection-------------------

selected_stock = ("AAPL", "BTC-USD", "AMZN","TSLA","SPY", "RIOT")
ticker_name = st.sidebar.selectbox("Select Company:", selected_stock)

# ---------------Load Data---------------------
@st.cache
def load_data(ticker_name=ticker_name, start=start, end=end):
    data = get_data(ticker_name, start, end)
    data.reset_index(inplace=True)
    return data

def non_sentiment_recommendation(ticker_name):
    response = requests.get(f'https://springstoneforrnngcp-2bu5nzzs7a-ew.a.run.app/predict?ticker={ticker_name}'
    )
    rec = response.json()['recommendation']
    return rec

# -----------Company Name-------------------


def company_name(ticker_name):
    if ticker_name == "BTC-USD":
        return "Bitcoin USD"
    cf = yf.Ticker(ticker_name)
    company_name = cf.info['longName']
    return company_name


st.header(company_name(ticker_name))


#---------------Recommendations section--------------

def sentiment(ticker_name):
    with st.spinner('Wait for sentiment analysis response...'):
        response2 = requests.get(
            f'https://springstoneforrnngcp-2bu5nzzs7a-ew.a.run.app/sentiment?ticker={ticker_name}'
        )
        senti = response2.json()['score']
    return senti


def sentiment_recommendation(ticker_name):
    with st.spinner('Wait for financial + sentiment recommendation...'):
        response2 = requests.get(
            f'https://springstoneforrnngcp-2bu5nzzs7a-ew.a.run.app/predict_enhanced?ticker={ticker_name}'
        )
        senti_rec = response2.json()['recommendation']
    return senti_rec


def recommendation():
    if st.button('Check Recommendations'):
        rec = non_sentiment_recommendation(ticker_name)
        senti = sentiment(ticker_name=ticker_name)
        senti_rec = sentiment_recommendation(ticker_name=ticker_name)
        with st.spinner('Wait for financial-based recommendation...'):
            st.markdown(
                f"**Financial based recommendation:** <font color=‘blue’>{rec}</font>",
            unsafe_allow_html=True)
        if float(senti) < -0.75:
            st.markdown(
                "<font color=‘blue’>The sentiment for this ticker is pretty negative for the last 7 days</font>",
                unsafe_allow_html=True)
        elif float(senti) > 0.75:
            st.markdown(
                "<font color=‘blue’>The sentiment for this ticker is pretty positive for the last 7 days</font>",
                unsafe_allow_html=True)
        else:
            st.markdown(
                "<font color=‘blue’>Hum... It is not so clear if the sentiment for this ticker is positive or negative for the last 7 days</font>",
                unsafe_allow_html=True)
        st.markdown(
            f"**Financial + sentiment recommendation:** <font color=‘blue’>{senti_rec}</font>",
            unsafe_allow_html=True)


recommendation()



# ----------Indicator Selection----------------

st.text("")
ma_flag = st.sidebar.checkbox("Moving Average", value=False)
if ma_flag:
    period = st.sidebar.slider("Choose Period", min_value=7, max_value=100)
st.text("")


# ------------Plot Functions-------------------

chart_width = st.expander(label="Adjust Chart Size").slider("", 1000, 2800, 880)

def plot_candlestick(ma_flag = False, bb_flag = False):
    fig = go.Figure(data=[go.Candlestick(x=load_data()['Date'],
            open=load_data()['Open'],
            high=load_data()['High'],
            low=load_data()['Low'],
            close=load_data()['Close'])])

    fig.update_traces(name="Candlestick", selector=dict(type='candlestick'))

    if ma_flag:
        ma_data = moving_average(load_data(),'Close',period)
        fig.add_trace(
            go.Scatter(
            x=ma_data["Date"],
            y=ma_data[f"Close_ma{int(period)}"],
            mode="markers+lines",
            name=f"{period} Day Moving Average",
            line=dict(
                color="blue")))

    fig.update_layout(
            width=chart_width,
            margin=dict(l=0, r=0, t=0, b=0, pad=0),
            legend=dict(
                x=0,
                y=0.99,
                traceorder="normal",
                font=dict(size=12),
            ),
            autosize=False,
            template="plotly_dark",)

    fig.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.8
    ))
    st.markdown("### Candlestick Graph")
    st.plotly_chart(fig)


plot_candlestick(ma_flag)

def relativeret(data):
    rel = data.pct_change()
    cumret = (1+rel).cumprod() - 1
    cumret = cumret.fillna(0)
    return cumret

def plot_raw_data():
    selected_stock = ("AAPL", "BTC-USD", "AMZN","TSLA","SPY", "RIOT")
    st.sidebar.write("Compare stock returns:")
    name = st.sidebar.multiselect("Add stock:", selected_stock, default=ticker_name)
    data = relativeret(get_data(name, start, end)['Close'])
    st.markdown("### Cumulative Return Comparison")
    st.line_chart(data)

plot_raw_data()
