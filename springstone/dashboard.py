import streamlit as st
from data import get_data
from plot import relative_plot
import pandas as pd
import numpy as np
from plotly import graph_objs as go
import datetime as dt
from datetime import date
from utils import basic_recommendation

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
ticker_name = st.sidebar.selectbox("Select Company", selected_stock)
rec = st.button("Strong Buy")

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

def plot_candlestick(ma_flag=False):
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

def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='Stock_Open'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Stock_Close'))

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

plot_raw_data()
