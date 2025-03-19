from flask import Flask, render_template, request, jsonify
import pandas as pd
from forecasting.visualization import plot_time_series
from forecasting.stationarity_tests import adf_test, kpss_test
from forecasting.moving_averages import moving_average_plots
from forecasting.acf_pacf import plot_acf_pacf
from forecasting.models import run_models
from forecasting.metrics import calculate_metrics
from forecasting.interpretations import interpret_acf_pacf

app = Flask(__name__)

DATA_FILE = "GlobalWeatherRepository.csv"
df = pd.read_csv(DATA_FILE)

df.columns = df.columns.str.lower()

if "last_updated" in df.columns:
    df.rename(columns={"last_updated": "date"}, inplace=True)
    df["date"] = pd.to_datetime(df["date"])

@app.route("/get_options")
def get_options():
    """Returns unique values for Country or Location dynamically."""
    category = request.args.get("type", "").lower()

    if category == "country" and "country" in df.columns:
        options = df["country"].dropna().unique().tolist()
    elif category == "location_name" and "location_name" in df.columns:
        options = df["location_name"].dropna().unique().tolist()
    else:
        options = []

    return jsonify({"options": options})
@app.route("/", methods=["GET", "POST"])
def index():
    countries = df["country"].unique().tolist() if "country" in df.columns else []
    locations = df["location_name"].unique().tolist() if "location_name" in df.columns else []

    if not countries:
        countries = ["No countries available"]
    if not locations:
        locations = ["No locations available"]

    return render_template("index.html", countries=countries, locations=locations)

@app.route("/forecast", methods=["POST"])
def forecast():
    global df

    if not all(key in request.form for key in ["category", "selected_value", "period"]):
        return "Error: Missing form fields. Ensure all fields are filled."

    category = request.form["category"].lower()
    selected_value = request.form["selected_value"]
    period = int(request.form["period"])

    if category not in df.columns:
        return f"Error: '{category}' column not found in dataset."

    filtered_df = df[df[category].str.lower() == selected_value.lower()]

    if "temperature_celsius" not in filtered_df.columns:
        return f"Error: 'temperature_celsius' column not found. Available columns: {filtered_df.columns}"

    if filtered_df.empty or len(filtered_df) < period:
        return f"Error: Not enough data for forecasting {period} steps."

    results = {
        "time_series_plot": plot_time_series(filtered_df, "temperature_celsius"),
        "acf_pacf_plot": plot_acf_pacf(filtered_df["temperature_celsius"]),
        "moving_average_plots": moving_average_plots(filtered_df, "temperature_celsius"),
        "adf_result": adf_test(filtered_df),
        "kpss_result": kpss_test(filtered_df),
        "arima_result": None,
        "sarima_result": None,
        "metrics": {"Error": "Forecasting failed."},
    }

    forecast_results = run_models(filtered_df, period, "temperature_celsius")

    if isinstance(forecast_results, dict):
        results["arima_result"] = forecast_results.get("ARIMA", "No ARIMA result")
        results["sarima_result"] = forecast_results.get("SARIMA", "No SARIMA result")
        results["arima_plot"] = forecast_results.get("ARIMA_PLOT", None)
        results["sarima_plot"] = forecast_results.get("SARIMA_PLOT", None)
        results["forecast_comparison"] = forecast_results.get("FORECAST_COMPARISON", None)

    results["moving_average_plots"] = moving_average_plots(filtered_df, "temperature_celsius")

    acf_values = [filtered_df["temperature_celsius"].autocorr()]
    pacf_values = [filtered_df["temperature_celsius"].diff().dropna().autocorr()]
    results["acf_pacf_interpretation"] = interpret_acf_pacf(acf_values, pacf_values)

    return render_template("results.html", results=results)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
