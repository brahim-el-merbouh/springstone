import streamlit as st
from data import get_data
from plot import relative_plot
import pandas as pd
import numpy as np
from plotly import graph_objs as go
import datetime as dt
from datetime import date
from springstone.utils import basic_recommendation
import matplotlib.pyplot as plt

# -----------Page Layout----------------------

st.set_page_config(layout="wide")
st.title("SpringStone Stock Prediction")

# -----------Date Input------------------------

today = dt.datetime.today()

start = st.sidebar.date_input('Start date:',
                                   today - dt.timedelta(days=365*1),
                                   min_value=today - dt.timedelta(days=365*10),
                                   max_value=today - dt.timedelta(days=31*2))
end = st.sidebar.date_input('End date:',
                                 min_value=start +
                                 dt.timedelta(days=31*2),
                                 max_value=today)

# -----------Stock Selection-------------------

selected_stock = np.array([ "AAPL", "BTC-USD", "BAC","TSLA","SPY"])
ticker_name = st.sidebar.multiselect("Select Company", selected_stock)

if st.button('Stock Recommendation'):
        with st.spinner("Generating Recommendation"):
            st.balloons()
            st.button('Strong Buy')

if ticker_name in selected_stock is "AAPL":
    st.button("Strong Buy")

# ----------Indicator Selection----------------

st.text("")
ma = st.sidebar.checkbox("Moving Average", value=False)
if ma:
    st.sidebar.text_input('Period')
bb = st.sidebar.checkbox("Bollinger Band", value=False)
if bb:
    st.sidebar.text_input('Period')
    st.sidebar.text_input('Standard Deviation')

data = get_data(ticker_name, start, end)
data.reset_index(inplace=True)

# ------------Plot Functions-------------------

chart_width = st.expander(label="Adjust Chart Size").slider("", 1000, 2800, 950)

def relativeret(data):
    rel = data.pct_change()
    cumret = (1+rel).cumprod() - 1
    cumret = cumret.fillna(0)
    cumret = cumret*100
    return cumret

def plot_raw_data():
    data = relativeret(get_data(ticker_name, start, end)['Close'])
    st.line_chart(data)

plot_raw_data()

def plot_candlestick():
    fig = go.Figure(data=[go.Candlestick(x=data['Date'],
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'])])

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
    st.plotly_chart(fig)

plot_candlestick()
