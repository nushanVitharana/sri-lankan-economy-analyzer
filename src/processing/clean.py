import pandas as pd

def clean_series(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Drop duplicate timestamps
    df = df[~df.index.duplicated(keep='first')]

    # Sort by time
    df = df.sort_index()

    # Convert all columns to numeric
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df


def drop_extreme_outliers(df: pd.DataFrame, z_thresh=5):
    """
    Optional: remove insane spikes (bad data, not real signals)
    """
    df = df.copy()

    for col in df.columns:
        z = (df[col] - df[col].mean()) / df[col].std()
        df.loc[z.abs() > z_thresh, col] = None

    return df