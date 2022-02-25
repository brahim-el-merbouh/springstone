import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

def relative_plot(df, x="Date", y="Close", title="Stock Price", ylabel="Closing Price (USD)", xlabel="Date", kind="line"):
    fig = sns.relplot(
        data=df,
        x=x,
        y=y,
        height=5,
        aspect=2.4,
        kind=kind
    ).set(
        title=title,
        ylabel=ylabel,
        xlabel=xlabel
    )
    st.pyplot(fig)

def plot_bollinger(df, column, standard_deviations):
    band1 = '{column}_bb{standard_deviations}'
    ### lower_band = f'{column}_bbl'
    ### middle_band = f'{column}_bbm'
    fig, ax = plt.subplots()
    sns.set(rc={'figure.figsize':(5,2.4)})
    ax = sns.lineplot(x="Date", y=band1, data = df)
    ### ax1 = sns.lineplot(x="Date", y=lower_band, data = df)
    ### ax2 = sns.lineplot(x="Date", y=middle_band, data = df)

def plot_moving_average(df, column, period):
    ma1 = f'{column}_ma{int(period)}'
    fig, ax = plt.subplots()
    sns.set(rc={'figure.figsize':(5,2.4)})
    ax = sns.lineplot(x="Date", y=ma1, data = df)
    ax.legend(loc='upper right', bbox_to_anchor=(1.4, 1))
