from email.policy import default
import streamlit as st
from data import get_data
import pandas as pd
import numpy as np
from plotly import graph_objs as go
import datetime as dt
from datetime import date
from springstone.utils import basic_recommendation, moving_average, bollinger_bands
import matplotlib.pyplot as plt
import yfinance as yf
import requests

# -----------Page Layout----------------------

st.set_page_config(layout="wide")
st.title("SpringStone Stock Prediction")

# -----------Date Input------------------------

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

selected_stock = ("AAPL", "BTC-USD", "BAC","TSLA","SPY", "RIOT")
ticker_name = st.sidebar.selectbox("Select Company", selected_stock)

# ---------------Load Data---------------------

data = get_data(ticker_name, start, end)
data.reset_index(inplace=True)

#rec = requests.get("http://localhost:8000/predict?ticker={ticker_name}")
rec = basic_recommendation(ticker_name)
st.button(rec)

# -----------Company Name-------------------

def company_name(ticker_name):
    if ticker_name == "BTC-USD":
        return "Bitcoin USD"
    cf = yf.Ticker(ticker_name)
    company_name = cf.info['longName']
    return company_name

st.header(company_name(ticker_name))

# ----------Indicator Selection----------------

st.text("")
ma_flag = st.sidebar.checkbox("Moving Average", value=False)
if ma_flag:
    period = st.sidebar.slider("Choose Period", min_value=7, max_value=100)
st.text("")
bb_flag = st.sidebar.checkbox("Bollinger Band", value=False)
if bb_flag:
    sd = st.sidebar.text_input('Standard Deviation')


# ------------Plot Functions-------------------

chart_width = st.expander(label="Adjust Chart Size").slider("", 1000, 2800, 880)

def plot_candlestick(ma_flag = False):
    fig = go.Figure(data=[go.Candlestick(x=data['Date'],
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'])])

    fig.update_traces(name="Candlestick", selector=dict(type='candlestick'))

    if ma_flag:
        ma_data = moving_average(data,'Close',period)
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
    st.text("Candlestick Graph")
    st.plotly_chart(fig)

plot_candlestick(ma_flag)

def relativeret(data):
    rel = data.pct_change()
    cumret = (1+rel).cumprod() - 1
    cumret = cumret.fillna(0)
    return cumret

def plot_raw_data():
    selected_stock = ("AAPL", "BTC-USD", "BAC","TSLA","SPY", "RIOT")
    name = st.sidebar.multiselect("Compare Company", selected_stock, default=ticker_name)
    data = relativeret(get_data(name, start, end)['Close'])
    st.text("Cumulative Return Comparison")
    st.line_chart(data)

plot_raw_data()
