import pandas as pd

def create_lags(df: pd.DataFrame, column: str, lags: list) -> pd.DataFrame:
    df = df.copy()

    for lag in lags:
        df[f"{column}_lag_{lag}"] = df[column].shift(lag)

    return df


def create_multiple_lags(df: pd.DataFrame, lag_map: dict) -> pd.DataFrame:
    """
    lag_map = {
        "reserves": [1, 3, 6, 12, 24],
        "inflation": [1, 3, 6]
    }
    """
    df = df.copy()

    for col, lags in lag_map.items():
        df = create_lags(df, col, lags)

    return df