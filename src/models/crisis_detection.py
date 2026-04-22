import pandas as pd

def detect_crisis_point(series: pd.Series, method="max_drop"):
    """
    Define crisis as biggest drop (e.g. FX crash)
    """

    if method == "max_drop":
        returns = series.pct_change()
        crisis_date = returns.idxmin()

    elif method == "max_volatility":
        vol = returns.rolling(6).std()
        crisis_date = vol.idxmax()

    else:
        raise ValueError("Unknown method")

    return crisis_date


def normalize_to_crisis(df: pd.DataFrame, crisis_date):
    df = df.copy()

    df["t"] = (df.index - crisis_date).days / 30
    df["t"] = df["t"].round().astype(int)

    return df