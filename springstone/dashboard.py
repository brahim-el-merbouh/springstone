import streamlit as st
from data import get_data
from plot import relative_plot
import pandas as pd
import numpy as np

st.title("SpringStone")

#Get user input where value is the stock symbol
value = st.sidebar.text_input("Stock Symbol", value = "AAPL")

# Get data
df = get_data(value)

# Get image of technical chart from finviz
st.text(f"{value} Share Price")
st.image (f"https://finviz.com/chart.ashx?t={value}")
st.write("#")

# Get our graph from plot
relative_plot(df)
