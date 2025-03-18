from statsmodels.tsa.stattools import adfuller, kpss

def adf_test(df):
    result = adfuller(df["temperature_celsius"])
    return {"ADF Statistic": result[0], "p-value": result[1]}

def kpss_test(df):
    result = kpss(df["temperature_celsius"], regression="c")
    return {"KPSS Statistic": result[0], "p-value": result[1]}
