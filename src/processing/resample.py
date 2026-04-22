import pandas as pd

def to_monthly(df: pd.DataFrame, method="ffill") -> pd.DataFrame:
    """
    Convert any frequency → monthly
    """

    df = df.copy()

    # Ensure datetime index
    df.index = pd.to_datetime(df.index)

    # Resample to monthly
    df = df.resample("ME").mean()

    if method == "ffill":
        df = df.ffill()

    elif method == "interpolate":
        df = df.interpolate()

    return df


def align_start_date(df: pd.DataFrame, start_date: str):
    return df[df.index >= start_date]


def align_end_date(df: pd.DataFrame, end_date: str):
    return df[df.index <= end_date]