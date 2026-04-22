import pandas as pd

def rolling_z_score(series: pd.Series, window=12):
    mean = series.rolling(window).mean()
    std = series.rolling(window).std()

    return (series - mean) / std


def detect_anomalies(series: pd.Series, threshold=2.5):
    z = rolling_z_score(series)

    anomalies = series[z.abs() > threshold]

    return anomalies