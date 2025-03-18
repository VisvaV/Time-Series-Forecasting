from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np


def calculate_metrics(forecast):
    """Calculates MAE, RMSE, and MAPE metrics for the forecasted data."""

    if not isinstance(forecast, dict) or "ARIMA" not in forecast or "SARIMA" not in forecast:
        return {"Error": "Invalid forecast format"}

    arima_forecast = forecast.get("ARIMA", [])
    sarima_forecast = forecast.get("SARIMA", [])

    if not arima_forecast or len(arima_forecast) < 2:
        return {"Error": "ARIMA forecast data is too short"}
    if not sarima_forecast or len(sarima_forecast) < 2:
        return {"Error": "SARIMA forecast data is too short"}

    actual = arima_forecast[:-1]
    predicted = arima_forecast[1:]

    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    mape = np.mean(np.abs((np.array(actual) - np.array(predicted)) / np.array(actual))) * 100

    return {"MAE": mae, "RMSE": rmse, "MAPE": mape}
