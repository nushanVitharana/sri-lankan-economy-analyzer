import wbgapi as wb
import pandas as pd

class WorldBankClient:
    def __init__(self, start_year=2000, end_year=2025):
        self.start_year = start_year
        self.end_year = end_year

    def fetch_indicator(self, country: str, indicator: str) -> pd.DataFrame:
        """
        Fetch a single indicator for a country
        """
        df = wb.data.DataFrame(
            indicator,
            country,
            time=range(self.start_year, self.end_year)
        )

        df = df.T
        df.index = pd.to_datetime(df.index.str.replace('YR', ''), format="%Y")
        df.columns = [indicator]

        return df

    def fetch_multiple(self, country: str, indicators: dict) -> pd.DataFrame:
        """
        indicators = {
            "reserves": "FI.RES.TOTL.CD",
            "inflation": "FP.CPI.TOTL.ZG"
        }
        """
        frames = []

        for name, code in indicators.items():
            df = self.fetch_indicator(country, code)
            df.columns = [name]
            frames.append(df)

        result = pd.concat(frames, axis=1)

        return result.sort_index()