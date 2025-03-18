import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt

import seaborn as sns


def plot_time_series(df, column_name="temperature_celsius"):
    """Plots a time series graph with correct date formatting."""

    plt.figure(figsize=(10, 5))
    sns.lineplot(data=df, x=df["date"], y=df[column_name], color="blue", label="Actual Data")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.title("Time Series Plot")
    plt.xticks(rotation=45)
    plt.grid()

    plot_path = "static/time_series.png"
    plt.savefig(plot_path)
    plt.close()

    return plot_path
