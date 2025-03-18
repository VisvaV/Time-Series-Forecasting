import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX

def run_models(df, period, column_name="temperature_celsius"):
    """Runs ARIMA and SARIMA models, returns forecasts and plots."""

    results = {}
    y = df[column_name]
    future_dates = pd.date_range(start=df["date"].iloc[-1], periods=period+1, freq='D')[1:]

    try:
        arima_model = ARIMA(y, order=(5,1,0)).fit()
        arima_forecast = arima_model.forecast(steps=period)

        plt.figure(figsize=(10, 5))
        plt.plot(df["date"], y, label="Actual Data", color="blue")
        plt.plot(future_dates, arima_forecast, label="ARIMA Forecast", color="red")
        plt.xlabel("Date")
        plt.ylabel("Temperature (°C)")
        plt.title("ARIMA Model Forecast")
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid()

        arima_path = "static/arima_forecast.png"
        plt.savefig(arima_path)
        plt.close()

        results["ARIMA"] = arima_forecast.tolist()
        results["ARIMA_PLOT"] = arima_path

    except:
        results["ARIMA"] = "ARIMA model failed."
        results["ARIMA_PLOT"] = None

    try:
        sarima_model = SARIMAX(y, order=(5,1,0), seasonal_order=(1,1,1,12)).fit()
        sarima_forecast = sarima_model.forecast(steps=period)

        plt.figure(figsize=(10, 5))
        plt.plot(df["date"], y, label="Actual Data", color="blue")
        plt.plot(future_dates, sarima_forecast, label="SARIMA Forecast", color="green")
        plt.xlabel("Date")
        plt.ylabel("Temperature (°C)")
        plt.title("SARIMA Model Forecast")
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid()

        sarima_path = "static/sarima_forecast.png"
        plt.savefig(sarima_path)
        plt.close()

        results["SARIMA"] = sarima_forecast.tolist()
        results["SARIMA_PLOT"] = sarima_path

    except:
        results["SARIMA"] = "SARIMA model failed."
        results["SARIMA_PLOT"] = None

    if "ARIMA" in results and "SARIMA" in results:
        plt.figure(figsize=(10, 5))
        plt.plot(df["date"], y, label="Actual Data", color="blue")
        if isinstance(results["ARIMA"], list):
            plt.plot(future_dates, results["ARIMA"], label="ARIMA", color="red")
        if isinstance(results["SARIMA"], list):
            plt.plot(future_dates, results["SARIMA"], label="SARIMA", color="green")
        plt.xlabel("Date")
        plt.ylabel("Temperature (°C)")
        plt.title("Forecasts from Different Models")
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid()

        forecast_comparison_path = "static/forecast_comparison.png"
        plt.savefig(forecast_comparison_path)
        plt.close()

        results["FORECAST_COMPARISON"] = forecast_comparison_path

    return results
