import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import pandas as pd


def moving_average_plots(df, column_name="temperature_celsius"):
    """Generates SMA, CMA, and EMA plots, saves them, and returns file paths."""

    df["SMA"] = df[column_name].rolling(window=5).mean()
    df["CMA"] = df[column_name].expanding().mean()
    df["EMA"] = df[column_name].ewm(span=5, adjust=False).mean()

    df = df.dropna(subset=["SMA", "CMA", "EMA"])

    plt.figure(figsize=(10, 5))
    plt.plot(df["date"], df[column_name], label="Actual Data", color="blue")
    plt.plot(df["date"], df["SMA"], label="Simple Moving Average (SMA)", color="red")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.title("Simple Moving Average (SMA)")
    plt.legend()
    sma_path = "static/sma_plot.png"
    plt.savefig(sma_path)
    plt.grid()
    plt.close()

    plt.figure(figsize=(10, 5))
    plt.plot(df["date"], df[column_name], label="Actual Data", color="blue")
    plt.plot(df["date"], df["CMA"], label="Cumulative Moving Average (CMA)", color="green")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.title("Cumulative Moving Average (CMA)")
    plt.legend()
    plt.grid()
    cma_path = "static/cma_plot.png"
    plt.savefig(cma_path)
    plt.close()

    plt.figure(figsize=(10, 5))
    plt.plot(df["date"], df[column_name], label="Actual Data", color="blue")
    plt.plot(df["date"], df["EMA"], label="Exponential Moving Average (EMA)", color="orange")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.title("Exponential Moving Average (EMA)")
    plt.legend()
    plt.grid()
    ema_path = "static/ema_plot.png"
    plt.savefig(ema_path)
    plt.close()

    return {"SMA": sma_path, "CMA": cma_path, "EMA": ema_path}
