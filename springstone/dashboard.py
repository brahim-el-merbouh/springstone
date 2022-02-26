from springstone.utils import moving_average
import streamlit as st
from data import get_data
from plot import relative_plot
import pandas as pd
import numpy as np
from plotly import graph_objs as go


#Get user input where value is the stock symbol
## value = st.sidebar.text_input("Stock Symbol", value = "AAPL")
st.set_page_config(layout="wide")

st.title("SpringStone Stock Prediction")
recc = st.button("Strong Buy")

selected_stock = st.sidebar.text_input("Select dataset for prediction", value = "TSLA")

start = st.sidebar.date_input('Start Date', value = pd.to_datetime("2012-02-18"))
end = st.sidebar.date_input('End Date', value = pd.to_datetime('2022-02-19'))
st.sidebar.text("")
period = st.sidebar.slider("Prediction Days:", 0, 30)
st.sidebar.text("")
ma = st.sidebar.checkbox("Moving Average", value=False)
if ma:
     st.sidebar.text_input('Period')
bb = st.sidebar.checkbox("Bollinger Band", value=False)
if bb:
     st.sidebar.text_input('Standard Deviation')

data = get_data(selected_stock, start, end)
data.reset_index(inplace=True)

ma_data = moving_average(data, column="Close", period = int(ma))

def plot_candlestick(ma_flag=False):
    fig = go.Figure(data=[go.Candlestick(x=data['Date'],
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'])])
    fig.layout.update(title_text="Candle Stick", xaxis_rangeslider_visible=True, autosize=False, width=800, height=500)
    if ma_flag:
        fig.add_trace(go.Scatter(x=ma_data['Date'], y=ma_data[f"Close_ma{int(period)}"], name='s'))
    st.plotly_chart(fig)

plot_candlestick()

def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='Stock_Open'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Stock_Close'))
    fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True, autosize=False, width=800, height=500)
    st.plotly_chart(fig)

plot_raw_data()
