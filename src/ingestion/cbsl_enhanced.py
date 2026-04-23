"""
Central Bank of Sri Lanka (CBSL) Data Client

This client currently provides deterministic synthetic data so the rest of the
pipeline can be developed and tested without relying on live APIs.
"""

from datetime import datetime
import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class CBSLClient:
    """Client for CBSL-style monetary and financial indicators."""

    def __init__(self, start_date="2000-01-01", end_date=None):
        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date) if end_date else datetime.now()

    def generate_synthetic_data(
        self,
        indicator_name: str,
        mean_value: float,
        std_dev: float,
        trend: float = 0.1,
        floor: float = 0.0,
    ) -> pd.Series:
        """
        Generate a stable synthetic monthly time series.
        """
        dates = pd.date_range(start=self.start_date, end=self.end_date, freq="ME")
        n = len(dates)
        seed = abs(hash(indicator_name)) % (2 ** 32)
        rng = np.random.default_rng(seed)

        random_walk = np.cumsum(rng.normal(0, std_dev, n))
        trend_component = np.linspace(
            0,
            (self.end_date - self.start_date).days / 365.25 * trend * mean_value,
            n,
        )
        seasonal = 0.05 * mean_value * np.sin(2 * np.pi * np.arange(n) / 12)
        values = mean_value + random_walk + trend_component + seasonal
        values = np.maximum(values, floor)

        series = pd.Series(values, index=dates, name=indicator_name)
        logger.info("Generated synthetic CBSL series for %s", indicator_name)
        return series

    def fetch_exchange_rate(self) -> pd.DataFrame:
        usd_lkr = self.generate_synthetic_data(
            "exchange_rate_usd",
            mean_value=250,
            std_dev=2.5,
            trend=0.04,
            floor=100,
        )
        return usd_lkr.to_frame()

    def fetch_money_supply(self) -> pd.DataFrame:
        money_supply = self.generate_synthetic_data(
            "money_supply_m2",
            mean_value=6000,
            std_dev=35,
            trend=0.08,
            floor=1000,
        )
        return money_supply.to_frame()

    def fetch_credit_private_sector(self) -> pd.DataFrame:
        credit = self.generate_synthetic_data(
            "credit_private_sector",
            mean_value=4000,
            std_dev=28,
            trend=0.06,
            floor=500,
        )
        return credit.to_frame()

    def fetch_interest_rates(self) -> pd.DataFrame:
        policy_rate = self.generate_synthetic_data(
            "policy_rate",
            mean_value=8.0,
            std_dev=0.08,
            trend=0.005,
            floor=2.0,
        )
        lending_rate = (policy_rate + 3.0).rename("base_lending_rate")
        treasury_bill_rate = (policy_rate + 1.4).rename("treasury_bill_rate")
        return pd.concat(
            [policy_rate, lending_rate.to_frame(), treasury_bill_rate.to_frame()],
            axis=1,
        )

    def fetch_banking_risk(self) -> pd.DataFrame:
        npl = self.generate_synthetic_data(
            "bank_npl_ratio",
            mean_value=4.5,
            std_dev=0.04,
            trend=0.015,
            floor=1.5,
        )
        return npl.to_frame()

    def fetch_stock_index(self) -> pd.DataFrame:
        aspi = self.generate_synthetic_data(
            "stock_index",
            mean_value=7000,
            std_dev=45,
            trend=0.03,
            floor=1000,
        )
        return aspi.to_frame()

    def fetch_all(self) -> pd.DataFrame:
        """
        Fetch all CBSL-style indicators and merge into a single DataFrame.
        """
        data_frames = [
            self.fetch_exchange_rate(),
            self.fetch_money_supply(),
            self.fetch_credit_private_sector(),
            self.fetch_interest_rates(),
            self.fetch_banking_risk(),
            self.fetch_stock_index(),
        ]

        result = pd.concat(data_frames, axis=1).ffill().bfill()
        logger.info(
            "Fetched all CBSL-style indicators (%s columns, %s rows)",
            result.shape[1],
            result.shape[0],
        )
        return result


class IMFProxyClient:
    """
    Placeholder for IMF-style indicators using proxy definitions.
    """

    def __init__(self):
        self.indicators = {
            "current_account": "NE.EXP.GNFS.CD",
            "external_debt_stock": "DT.DOD.DECT.GD.ZS",
            "international_reserves": "FI.RES.TOTL.CD",
            "terms_of_trade": "TT.PRI.MRCH.XD.WD",
        }
