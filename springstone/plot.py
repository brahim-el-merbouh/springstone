import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def relative_plot(df, x="Date", y="Close", title="Stock Price", ylabel="Closing Price (USD)", xlabel="Date", kind="line"):
    sns.relplot(
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

def plot_bollinger(df, column):
    upper_band = f'{column}_bbu'
    lower_band = f'{column}_bbl'
    middle_band = f'{column}_bbm'
    fig, ax = plt.subplots()
    ax = sns.lineplot(x="Date", y=upper_band, data = df)
    ax1 = sns.lineplot(x="Date", y=lower_band, data = df)
    ax2 = sns.lineplot(x="Date", y=middle_band, data = df)
