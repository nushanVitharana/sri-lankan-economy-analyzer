import pandas as pd

def rolling_stats(df: pd.DataFrame, column: str, window=12):
    df = df.copy()

    df[f"{column}_rolling_mean"] = df[column].rolling(window).mean()
    df[f"{column}_rolling_std"] = df[column].rolling(window).std()

    return df


def rolling_volatility(df: pd.DataFrame, column: str, window=12):
    df = df.copy()

    returns = df[column].pct_change()
    df[f"{column}_volatility"] = returns.rolling(window).std()

    return df