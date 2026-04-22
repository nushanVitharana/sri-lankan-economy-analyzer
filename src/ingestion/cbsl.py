import pandas as pd

class CBSLClient:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def load_excel(self, sheet_name=0) -> pd.DataFrame:
        df = pd.read_excel(self.filepath, sheet_name=sheet_name)
        return df

    def clean_time_series(self,
                          df: pd.DataFrame,
                          date_col: str,
                          value_col: str,
                          rename_to: str) -> pd.DataFrame:
        """
        Standardize CBSL messy formats
        """

        df = df[[date_col, value_col]].copy()

        # Handle weird date formats (e.g. "Jan-2020")
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

        df = df.dropna(subset=[date_col])
        df = df.set_index(date_col)

        # Convert to numeric (CBSL often has commas, text)
        df[value_col] = pd.to_numeric(df[value_col], errors='coerce')

        df.columns = [rename_to]

        return df.sort_index()

    def load_series(self, date_col, value_col, rename_to):
        raw = self.load_excel()
        return self.clean_time_series(raw, date_col, value_col, rename_to)