import pandas as pd

def merge_series(series_dict: dict) -> pd.DataFrame:
    """
    series_dict = {
        "reserves": df1,
        "fx_rate": df2,
        ...
    }
    """

    frames = []

    for name, df in series_dict.items():
        temp = df.copy()
        temp.columns = [name]
        frames.append(temp)

    merged = pd.concat(frames, axis=1)

    return merged.sort_index()


def trim_common_range(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove periods where most data is missing
    """

    df = df.copy()

    # Drop rows where ALL values are NaN
    df = df.dropna(how="all")

    return df