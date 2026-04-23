import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ingestion.config import INDICATOR_METADATA
from ingestion.data_manager import DataManager
from models.cross_correlation import compute_cross_correlation


class DashboardData:
    def __init__(self, path="../../data/processed/master.csv"):
        self.manager = DataManager(country="sri_lanka", start_year=2010, end_year=2025)
        self.df = self._load_dataframe(path)
        self.metadata = INDICATOR_METADATA
        self.risk_summary = self.manager.get_risk_summary()

    def _load_dataframe(self, path: str) -> pd.DataFrame:
        candidates = [
            path,
            os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                "data",
                "processed",
                "master.csv",
            ),
            os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                "data",
                "processed",
                "master_latest.csv",
            ),
        ]

        for candidate in candidates:
            if os.path.exists(candidate):
                df = pd.read_csv(candidate, index_col=0, parse_dates=True)
                if not df.empty:
                    return df

        return self.manager.fetch_all()

    def get_columns(self):
        return list(self.df.columns)

    def get_display_columns(self):
        preferred = [
            "reserves",
            "inflation",
            "debt",
            "exchange_rate_usd",
            "current_account_pct_gdp",
            "import_cover_months",
            "external_vulnerability_index",
            "fiscal_stress_index",
            "monetary_pressure_index",
            "household_stress_index",
            "macro_stress_index",
        ]
        available = [col for col in preferred if col in self.df.columns]
        return available or self.get_columns()

    def get_series(self, column):
        return self.df[column]

    def get_cross_corr(self, col1, col2):
        return compute_cross_correlation(self.df[col1], self.df[col2])

    def get_label(self, column: str) -> str:
        return self.metadata.get(column, {}).get("label", column.replace("_", " ").title())

    def get_unit(self, column: str) -> str:
        return self.metadata.get(column, {}).get("unit", "")

    def get_snapshot_cards(self):
        latest = self.df.ffill().iloc[-1]
        cards = [
            {
                "title": "Risk Regime",
                "value": self.risk_summary.get("risk_regime", "Unknown"),
                "subtitle": self.risk_summary.get("top_story", ""),
            },
            {
                "title": "Macro Stress",
                "value": self.risk_summary.get("macro_stress_index", "n/a"),
                "subtitle": "Composite index across external, fiscal, monetary and household stress",
            },
            {
                "title": "Import Cover",
                "value": self.risk_summary.get("import_cover_months", "n/a"),
                "subtitle": "Months of imports covered by reserves",
            },
            {
                "title": "Inflation",
                "value": self.risk_summary.get("inflation", round(float(latest.get("inflation", 0)), 2)),
                "subtitle": "Latest inflation pressure",
            },
        ]
        return cards
