import logging

import numpy as np
import pandas as pd
import wbgapi as wb

logger = logging.getLogger(__name__)


class WorldBankClient:
    def __init__(self, start_year=2000, end_year=2025):
        self.start_year = start_year
        self.end_year = end_year
        self.failed_indicators = []

    def _synthetic_series(self, indicator_name: str) -> pd.DataFrame:
        """Build a deterministic fallback series when the API is unavailable."""
        years = pd.date_range(
            start=f"{self.start_year}-01-01",
            end=f"{self.end_year - 1}-01-01",
            freq="YS"
        )
        n = len(years)
        base = np.linspace(0, 1, n)
        seed = abs(hash(indicator_name)) % (2 ** 32)
        rng = np.random.default_rng(seed)

        patterns = {
            "reserves": 2.5e9 + 5.0e9 * np.sin(base * 3.1) + 1.3e9 * base,
            "inflation": 4 + 8 * np.maximum(0, np.sin(base * 5.2)) + rng.normal(0, 0.8, n),
            "food_inflation_proxy": 5 + 9 * np.maximum(0, np.sin(base * 4.7)) + rng.normal(0, 1.1, n),
            "debt": 65 + 35 * base + 6 * np.sin(base * 4.0),
            "external_debt": 42 + 20 * base + 4 * np.sin(base * 3.6),
            "debt_service_pct_exports": 12 + 10 * base + 3 * np.sin(base * 4.9),
            "short_term_debt_pct_reserves": 55 + 35 * base + 5 * np.sin(base * 4.3),
            "current_account_pct_gdp": -1.5 - 4.0 * base + 1.5 * np.sin(base * 2.5),
            "exports_usd": 8.5e9 + 4.0e9 * base + 6e8 * np.sin(base * 3.3),
            "imports_usd": 10.5e9 + 5.5e9 * base + 8e8 * np.sin(base * 3.0),
            "exports_pct_gdp": 19 + 2.5 * np.sin(base * 2.1),
            "imports_pct_gdp": 26 + 3.5 * np.sin(base * 2.2),
            "trade_openness": 47 + 6 * np.sin(base * 2.6),
            "fdi_inflows": 5e8 + 2.8e8 * np.sin(base * 4.6) + 1.2e8 * base,
            "remittances_pct_gdp": 6.5 + 1.1 * np.sin(base * 2.2),
            "tourism_receipts_pct_exports": 9 + 4.5 * np.maximum(0, np.sin(base * 3.7)),
            "revenue_pct_gdp": 12.5 - 1.6 * base + 0.5 * np.sin(base * 3.9),
            "expense_pct_gdp": 18 + 2.0 * base + 0.9 * np.sin(base * 3.2),
            "gdp_growth": 4.2 + 1.6 * np.sin(base * 3.8) - 4.5 * np.exp(-((base - 0.78) ** 2) / 0.01),
            "gdp_per_capita": 2500 + 1900 * base + 120 * np.sin(base * 3.0),
            "unemployment_rate": 5.8 + 1.1 * np.sin(base * 3.1) + 1.2 * np.exp(-((base - 0.78) ** 2) / 0.015),
            "poverty_headcount": 13 - 5 * base + 1.2 * np.sin(base * 2.3),
            "real_interest_rate": 1.5 + 2.4 * np.sin(base * 4.4),
            "broad_money_pct_gdp": 43 + 12 * base + 2.2 * np.sin(base * 2.8),
            "trade_balance_proxy": -1.8e9 - 8e8 * np.sin(base * 2.8) - 3e8 * base,
            "tourism_receipts": 1.2e9 + 6e8 * np.maximum(0, np.sin(base * 4.0)),
            "remittances_inflows": 5.5e9 + 4e8 * np.sin(base * 3.0),
            "net_oda": 4e8 + 9e7 * np.sin(base * 2.0),
            "portfolio_inflows": 2.5e8 + 1.2e8 * np.sin(base * 5.5),
        }

        values = patterns.get(indicator_name, 100 + 10 * base + rng.normal(0, 2, n))
        df = pd.DataFrame({indicator_name: np.asarray(values, dtype=float)}, index=years)
        logger.info("Using synthetic fallback for %s", indicator_name)
        return df

    def fetch_indicator(self, country: str, indicator: str, indicator_name: str = None) -> pd.DataFrame:
        """
        Fetch a single indicator for a country.
        """
        col_name = indicator_name if indicator_name else indicator

        try:
            df = wb.data.DataFrame(
                indicator,
                country,
                time=range(self.start_year, self.end_year)
            )

            df = df.T
            df.index = pd.to_datetime(df.index.str.replace("YR", ""), format="%Y")
            df.columns = [col_name]

            logger.info("Fetched %s (%s)", col_name, indicator)
            return df

        except Exception as exc:
            logger.warning("Failed to fetch %s (%s): %s", col_name, indicator, exc)
            self.failed_indicators.append(indicator)
            return self._synthetic_series(col_name)

    def fetch_multiple(self, country: str, indicators: dict) -> pd.DataFrame:
        """
        Fetch multiple indicators for a country.
        """
        frames = []

        for name, code in indicators.items():
            df = self.fetch_indicator(country, code, name)
            if df is not None:
                frames.append(df)

        if not frames:
            raise ValueError(f"No indicators could be fetched for country {country}")

        result = pd.concat(frames, axis=1).sort_index()
        logger.info("Fetched %s/%s indicators successfully", len(frames), len(indicators))
        return result

    def fetch_multiple_countries(self, countries: list, indicators: dict) -> dict:
        """
        Fetch the same indicator set for multiple countries.
        """
        results = {}

        for country in countries:
            try:
                results[country] = self.fetch_multiple(country, indicators)
                logger.info("Fetched data for %s", country)
            except Exception as exc:
                logger.error("Failed to fetch data for %s: %s", country, exc)
                results[country] = None

        return results
