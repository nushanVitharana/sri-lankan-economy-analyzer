import pandas as pd

from src.processing.clean import clean_series
from src.processing.resample import to_monthly
from src.processing.align import merge_series, trim_common_range
from src.processing.validate import check_missing, check_date_range


def process_series(df: pd.DataFrame) -> pd.DataFrame:
    df = clean_series(df)
    df = to_monthly(df)
    return df


def build_master_dataset(series_dict: dict) -> pd.DataFrame:
    """
    series_dict example:
    {
        "reserves": df_reserves,
        "fx_rate": df_fx,
        "inflation": df_inf,
        "debt": df_debt
    }
    """

    processed = {}

    # Step 1: clean + resample each
    for name, df in series_dict.items():
        processed[name] = process_series(df)

    # Step 2: merge all
    master = merge_series(processed)

    # Step 3: trim bad rows
    master = trim_common_range(master)

    # Step 4: optional forward fill
    master = master.ffill()

    # Step 5: validation
    check_missing(master)
    check_date_range(master)

    return master


def save_master_dataset(df: pd.DataFrame, path: str):
    df.to_csv(path)
    print(f"Saved dataset to {path}")