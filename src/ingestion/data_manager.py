"""
Unified Data Manager for all data sources.
"""

from datetime import datetime
import logging
import os
import sys
from typing import Dict, Optional

import numpy as np
import pandas as pd

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from features.risk_enrichment import build_risk_summary, enrich_dataset
from ingestion.cbsl_enhanced import CBSLClient
from ingestion.config import (
    ALTERNATIVE_INDICATORS,
    COMPARATOR_COUNTRIES,
    COUNTRIES,
    INDICATOR_METADATA,
    WORLD_BANK_INDICATORS,
)
from ingestion.world_bank import WorldBankClient
from models.forecasting import ARIMAForecaster, VARForecaster, save_forecasts


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class DataManager:
    """
    Unified manager for economic data sources and enrichment.
    """

    def __init__(self, country: str = "sri_lanka", start_year: int = 2000, end_year: int = 2025):
        country_lower = country.lower()
        if country_lower in COUNTRIES:
            self.country = country_lower
            self.country_code = COUNTRIES[country_lower]
        else:
            self.country = country
            self.country_code = country

        self.start_year = start_year
        self.end_year = end_year
        self.wb_client = WorldBankClient(start_year, end_year)
        self.cbsl_client = CBSLClient(start_date=f"{start_year}-01-01", end_date=f"{end_year}-12-31")
        self.data_cache = {}
        logger.info("DataManager initialized for %s", self.country_code)

    def fetch_world_bank(self, indicators: Optional[Dict] = None) -> pd.DataFrame:
        indicators = indicators or WORLD_BANK_INDICATORS
        df = self.wb_client.fetch_multiple(self.country_code, indicators)
        self.data_cache["world_bank"] = df
        return df

    def fetch_alternative_sources(self) -> pd.DataFrame:
        df = self.wb_client.fetch_multiple(self.country_code, ALTERNATIVE_INDICATORS)
        self.data_cache["alternative"] = df
        return df

    def fetch_cbsl(self) -> pd.DataFrame:
        df = self.cbsl_client.fetch_all()
        df_annual = df.resample("YE").last()
        df_annual.index = pd.to_datetime(df_annual.index.year, format="%Y")
        self.data_cache["cbsl"] = df_annual
        return df_annual

    def fetch_all(
        self,
        include_world_bank: bool = True,
        include_alternative: bool = True,
        include_cbsl: bool = True,
        enrich: bool = True,
    ) -> pd.DataFrame:
        frames = []

        if include_world_bank:
            frames.append(self.fetch_world_bank())
        if include_alternative:
            frames.append(self.fetch_alternative_sources())
        if include_cbsl:
            frames.append(self.fetch_cbsl())

        frames = [frame for frame in frames if frame is not None and not frame.empty]
        if not frames:
            logger.error("No data could be fetched from any source")
            return pd.DataFrame()

        merged = pd.concat(frames, axis=1).sort_index()
        merged = merged.loc[:, ~merged.columns.duplicated()]
        merged = merged.ffill().bfill()

        if enrich:
            merged = enrich_dataset(merged)

        self.data_cache["merged"] = merged
        logger.info("Merged dataset ready: %s rows x %s columns", merged.shape[0], merged.shape[1])
        return merged

    def get_metadata(self) -> pd.DataFrame:
        merged = self.data_cache.get("merged")
        columns = merged.columns.tolist() if isinstance(merged, pd.DataFrame) else []
        rows = []
        for col in columns:
            info = INDICATOR_METADATA.get(col, {})
            rows.append(
                {
                    "indicator": col,
                    "label": info.get("label", col.replace("_", " ").title()),
                    "unit": info.get("unit", "index"),
                    "category": info.get("category", "Derived"),
                }
            )
        return pd.DataFrame(rows)

    def get_summary(self) -> Dict:
        merged = self.data_cache.get("merged")
        summary = {
            "country": self.country_code,
            "data_sources": [key for key in self.data_cache.keys() if key != "merged"],
            "total_rows": 0,
            "total_columns": 0,
            "indicators": [],
            "date_range": None,
            "risk_summary": {},
        }

        if isinstance(merged, pd.DataFrame) and not merged.empty:
            summary["total_rows"] = len(merged)
            summary["total_columns"] = len(merged.columns)
            summary["indicators"] = merged.columns.tolist()
            summary["date_range"] = f"{merged.index.min().year} - {merged.index.max().year}"
            summary["risk_summary"] = build_risk_summary(merged)

        return summary

    def get_risk_summary(self) -> Dict:
        merged = self.data_cache.get("merged")
        if merged is None or merged.empty:
            merged = self.fetch_all()
        return build_risk_summary(merged)

    def get_comparator_snapshot(self, indicators: Optional[list] = None) -> pd.DataFrame:
        indicators = indicators or [
            "inflation",
            "debt",
            "current_account_pct_gdp",
            "gdp_growth",
        ]
        comparator_data = self.wb_client.fetch_multiple_countries(COMPARATOR_COUNTRIES, {
            key: value for key, value in WORLD_BANK_INDICATORS.items() if key in indicators
        })

        rows = []
        for country, df in comparator_data.items():
            if df is None or df.empty:
                continue
            latest = df.ffill().iloc[-1]
            row = {"country": country}
            row.update({indicator: latest.get(indicator) for indicator in indicators})
            rows.append(row)

        return pd.DataFrame(rows)

    def forecast_all(self, steps: int = 5, save_results: bool = True) -> Dict:
        df_all = self.fetch_all()
        if df_all.empty:
            logger.error("No data available for forecasting")
            return {}

        numeric = df_all.select_dtypes(include=[np.number]).dropna(axis=1, how="all")
        results = {
            "arima_forecasts": {},
            "var_forecasts": {},
            "metadata": {
                "forecast_steps": steps,
                "indicators": list(numeric.columns),
                "data_points": len(numeric),
            },
        }

        arima_forecaster = ARIMAForecaster()
        for column in numeric.columns[:12]:
            try:
                forecast = arima_forecaster.fit_predict(numeric[column], column, steps)
                if not forecast.empty:
                    results["arima_forecasts"][column] = forecast
            except Exception as exc:
                logger.error("ARIMA forecast error for %s: %s", column, exc)

        try:
            var_forecaster = VARForecaster()
            limited = numeric.iloc[:, : min(8, numeric.shape[1])].dropna()
            if not limited.empty and limited.shape[1] >= 2:
                results["var_forecasts"] = var_forecaster.fit_predict(limited, steps)
        except Exception as exc:
            logger.error("VAR forecast error: %s", exc)

        if save_results:
            os.makedirs("data/forecasts", exist_ok=True)
            if results["arima_forecasts"]:
                save_forecasts(
                    results["arima_forecasts"],
                    f"data/forecasts/arima_forecasts_{self.country_code}_{steps}steps.xlsx",
                )
            if results["var_forecasts"]:
                save_forecasts(
                    results["var_forecasts"],
                    f"data/forecasts/var_forecasts_{self.country_code}_{steps}steps.xlsx",
                )

        return results


def analyze_forecast_trend(forecast_df: pd.DataFrame) -> Dict:
    values = forecast_df["forecast"].values
    if len(values) < 2:
        return {"trend": "insufficient_data", "direction": "unknown"}

    slope = np.polyfit(range(len(values)), values, 1)[0]
    avg_value = np.mean(values)
    volatility = np.std(values) / abs(avg_value) if avg_value != 0 else 0

    if abs(slope) < volatility * 0.1:
        trend = "stable"
        direction = "flat"
    elif slope > 0:
        trend = "increasing"
        direction = "up"
    else:
        trend = "decreasing"
        direction = "down"

    return {
        "trend": trend,
        "direction": direction,
        "slope": slope,
        "avg_value": avg_value,
        "volatility": volatility,
        "confidence_range": forecast_df["upper_ci"].max() - forecast_df["lower_ci"].min(),
    }


def get_indicator_category(indicator: str) -> str:
    return INDICATOR_METADATA.get(indicator, {}).get("category", "Derived")


def format_forecast_display(indicator: str, forecast_df: pd.DataFrame, model_type: str = "ARIMA"):
    trend_analysis = analyze_forecast_trend(forecast_df)
    category = get_indicator_category(indicator)

    print(f"\n{'=' * 80}")
    print(f"{model_type.upper()} FORECAST: {indicator.upper()}")
    print(f"{'=' * 80}")
    print(f"Category: {category}")
    print(f"Forecast Period: {forecast_df.index[0].year} - {forecast_df.index[-1].year}")
    print(f"Trend: {trend_analysis['trend'].title()}")
    print(f"Average Forecast: {trend_analysis['avg_value']:.2f}")
    print(f"Volatility: {trend_analysis['volatility']:.1%}")
    print(f"Confidence Range: +/-{trend_analysis['confidence_range']:.2f}")


def generate_executive_summary(forecast_results: Dict, df_historical: pd.DataFrame):
    arima_forecasts = forecast_results.get("arima_forecasts", {})
    var_forecasts = forecast_results.get("var_forecasts", {})

    print(f"\n{'=' * 100}")
    print("EXECUTIVE SUMMARY - SRI LANKA ECONOMIC FORECASTS")
    print(f"{'=' * 100}")
    print(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Analysis Period: {len(df_historical)} historical years")
    print(f"Forecast Horizon: {len(list(arima_forecasts.values())[0]) if arima_forecasts else 0} years")
    print(f"Indicators Analyzed: {len(arima_forecasts)}")
    print(f"VAR Models: {len(var_forecasts)}")
