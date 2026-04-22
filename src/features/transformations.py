import pandas as pd
import numpy as np

def pct_change(df: pd.DataFrame, columns: list, periods=1) -> pd.DataFrame:
    df = df.copy()

    for col in columns:
        df[f"{col}_pct_{periods}"] = df[col].pct_change(periods)

    return df


def log_transform(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    df = df.copy()

    for col in columns:
        df[f"log_{col}"] = np.log(df[col])

    return df


def diff(df: pd.DataFrame, columns: list, periods=1) -> pd.DataFrame:
    df = df.copy()

    for col in columns:
        df[f"{col}_diff_{periods}"] = df[col].diff(periods)

    return df