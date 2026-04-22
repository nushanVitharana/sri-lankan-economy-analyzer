import pandas as pd

from models.cross_correlation import compute_cross_correlation

class DashboardData:

    def __init__(self, path="../data/processed/master.csv"):
        self.df = pd.read_csv(path, index_col=0, parse_dates=True)

    def get_columns(self):
        return list(self.df.columns)

    def get_series(self, column):
        return self.df[column]

    def get_cross_corr(self, col1, col2):
        return compute_cross_correlation(
            self.df[col1],
            self.df[col2]
        )