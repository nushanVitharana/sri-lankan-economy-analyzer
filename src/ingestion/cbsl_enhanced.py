"""
Central Bank of Sri Lanka (CBSL) Data Client

This module provides access to CBSL economic data including:
- Exchange rates (USD/LKR)
- Money supply (M1, M2, M3)
- Credit to private sector
- Interest rates
- Stock market indices

Note: Currently uses synthetic/mock data. In production, this would:
1. Connect to CBSL REST API: https://www.cbsl.gov.lk/
2. Use CBSL publication downloads
3. Integrate with other official sources
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class CBSLClient:
    """Client for Central Bank of Sri Lanka data"""

    def __init__(self, start_date="2000-01-01", end_date=None):
        """
        Initialize CBSL client

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (defaults to today)
        """
        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date) if end_date else datetime.now()

    def generate_synthetic_data(self, indicator_name: str,
                               mean_value: float,
                               std_dev: float,
                               trend: float = 0.1) -> pd.Series:
        """
        Generate realistic synthetic time series data

        Args:
            indicator_name: Name of the indicator
            mean_value: Mean value of the series
            std_dev: Standard deviation
            trend: Linear trend component (% per year)

        Returns:
            Pandas Series with monthly data
        """
        # Generate monthly date range
        dates = pd.date_range(start=self.start_date, end=self.end_date, freq='ME')

        # Generate base random walk
        n = len(dates)
        random_walk = np.cumsum(np.random.normal(0, std_dev, n))

        # Add trend
        trend_component = np.linspace(0, (self.end_date - self.start_date).days / 365.25 * trend * mean_value, n)

        # Combine components
        values = mean_value + random_walk + trend_component

        # Add seasonal component (for some indicators)
        seasonal = 0.05 * mean_value * np.sin(2 * np.pi * np.arange(n) / 12)
        values = values + seasonal

        # Ensure positive values
        values = np.abs(values)

        series = pd.Series(values, index=dates, name=indicator_name)
        logger.info(f"✓ Generated synthetic data for {indicator_name}")

        return series

    def fetch_exchange_rate(self) -> pd.DataFrame:
        """
        Fetch USD/LKR exchange rate data

        Returns:
            DataFrame with exchange rate
        """
        # In 2024, USD/LKR traded ~320-330 LKR per USD
        # Historical data: from ~120 in 2020 to ~320 by 2024
        usd_lkr = self.generate_synthetic_data(
            "usd_lkr",
            mean_value=250,  # Average ~250 LKR per USD
            std_dev=15,       # Moderate volatility
            trend=0.05        # Depreciation trend
        )
        return usd_lkr.to_frame()

    def fetch_money_supply(self, measure: str = "m2") -> pd.DataFrame:
        """
        Fetch money supply data (M1, M2, or M3)

        Args:
            measure: 'm1', 'm2', or 'm3' (default: 'm2')

        Returns:
            DataFrame with money supply in LKR billions
        """
        # Sri Lanka M2 was ~5000-7000 Bn LKR by 2024
        mean_values = {
            "m1": 1000,   # ~1000 Bn LKR
            "m2": 6000,   # ~6000 Bn LKR
            "m3": 8000    # ~8000 Bn LKR
        }

        measure_lower = measure.lower()
        mean = mean_values.get(measure_lower, 6000)

        money_supply = self.generate_synthetic_data(
            f"money_supply_{measure.upper()}",
            mean_value=mean,
            std_dev=mean * 0.1,
            trend=0.08  # M2 growing ~8% annually
        )
        return money_supply.to_frame()

    def fetch_credit_private_sector(self) -> pd.DataFrame:
        """
        Fetch credit to private sector (LKR billions)

        Returns:
            DataFrame with private sector credit
        """
        # Private sector credit was ~3500-4500 Bn LKR by 2024
        credit = self.generate_synthetic_data(
            "credit_private_sector",
            mean_value=4000,
            std_dev=300,
            trend=0.06  # Growing ~6% annually
        )
        return credit.to_frame()

    def fetch_interest_rates(self) -> pd.DataFrame:
        """
        Fetch key interest rates (%)

        Returns:
            DataFrame with REPO rate (policy rate) and lending rate
        """
        # CBSL repo rate varies 5-10% depending on inflation
        repo_rate = self.generate_synthetic_data(
            "repo_rate",
            mean_value=7.5,
            std_dev=1.5,
            trend=0.01
        )

        # Lending rate typically 2-3% above repo rate
        lending_rate = repo_rate + np.random.normal(2.5, 0.3, len(repo_rate))
        lending_rate.name = "base_lending_rate"

        return pd.concat([repo_rate, lending_rate.to_frame()], axis=1)

    def fetch_stock_index(self) -> pd.DataFrame:
        """
        Fetch All Share Price Index (ASPI)

        Returns:
            DataFrame with stock index value
        """
        # ASPI was ~6500-7500 by 2024
        aspi = self.generate_synthetic_data(
            "all_share_index",
            mean_value=7000,
            std_dev=500,
            trend=0.03  # Growing ~3% annually
        )
        return aspi.to_frame()

    def fetch_all(self) -> pd.DataFrame:
        """
        Fetch all CBSL indicators and merge into single DataFrame

        Returns:
            DataFrame with all CBSL indicators
        """
        data_frames = []

        # Fetch all indicators
        data_frames.append(self.fetch_exchange_rate())
        data_frames.append(self.fetch_money_supply("m2"))
        data_frames.append(self.fetch_credit_private_sector())
        data_frames.append(self.fetch_interest_rates())
        data_frames.append(self.fetch_stock_index())

        # Merge all data
        result = pd.concat(data_frames, axis=1)
        result = result.ffill().bfill()  # Forward fill then backward fill

        logger.info(f"✓ Fetched all CBSL indicators ({result.shape[1]} columns, {result.shape[0]} rows)")

        return result


class IMFProxyClient:
    """
    Proxy client for IMF-style indicators using World Bank data

    Since real IMF API access requires authentication, this uses WB proxies
    for similar indicators.
    """

    def __init__(self):
        self.indicators = {
            "current_account": "NE.EXP.GNFS.CD",  # Exports proxy
            "external_debt_stock": "DT.DOD.DECT.GD.ZS",
            "international_reserves": "FI.RES.TOTL.CD",
            "terms_of_trade": "TT.PRI.MRCH.XD.WD",
        }


# Example usage
if __name__ == "__main__":
    # Test CBSL client
    cbsl = CBSLClient()

    print("\n" + "="*60)
    print("CBSL Economic Indicators (Synthetic Data for Demo)")
    print("="*60 + "\n")

    # Fetch all indicators
    df_cbsl = cbsl.fetch_all()
    print(f"Shape: {df_cbsl.shape}")
    print("\nLatest values:")
    print(df_cbsl.tail())
    print(f"\nColumns: {list(df_cbsl.columns)}")

