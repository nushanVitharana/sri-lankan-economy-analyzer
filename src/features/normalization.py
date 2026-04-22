import pandas as pd

def z_score(df: pd.DataFrame, column: str, window=None):
    df = df.copy()

    if window:
        mean = df[column].rolling(window).mean()
        std = df[column].rolling(window).std()
    else:
        mean = df[column].mean()
        std = df[column].std()

    df[f"{column}_z"] = (df[column] - mean) / std

    return df


def base_index(df: pd.DataFrame, column: str, base_date):
    df = df.copy()

    base_value = df.loc[base_date, column]
    df[f"{column}_indexed"] = df[column] / base_value * 100

    return df