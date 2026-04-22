import pandas as pd

class IMFClient:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def load_csv(self) -> pd.DataFrame:
        df = pd.read_csv(self.filepath)

        return df

    def standardize(self, df: pd.DataFrame,
                    date_col: str,
                    value_col: str,
                    rename_to: str) -> pd.DataFrame:
        """
        Converts raw IMF format → clean time series
        """

        df = df[[date_col, value_col]].copy()

        df[date_col] = pd.to_datetime(df[date_col])
        df = df.set_index(date_col)

        df.columns = [rename_to]

        return df.sort_index()

    def load_series(self, date_col, value_col, rename_to):
        raw = self.load_csv()
        return self.standardize(raw, date_col, value_col, rename_to)