"""
Unified Data Manager for all data sources

This module orchestrates fetching data from multiple sources:
- World Bank (12+ economic indicators)
- CBSL (5+ monetary/financial indicators)
- Alternative sources (tourism, remittances, etc.)

Usage:
    manager = DataManager(country="LKA")
    df_comprehensive = manager.fetch_all()
    df_world_bank = manager.fetch_world_bank()
    df_cbsl = manager.fetch_cbsl()
"""

import pandas as pd
import logging
from typing import Dict, Optional
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ingestion.world_bank import WorldBankClient
from ingestion.cbsl_enhanced import CBSLClient
from ingestion.config import (
    WORLD_BANK_INDICATORS,
    ALTERNATIVE_INDICATORS,
    COUNTRIES
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataManager:
    """
    Unified manager for all economic data sources
    """

    def __init__(self, country: str = "sri_lanka", start_year: int = 2000, end_year: int = 2025):
        """
        Initialize DataManager

        Args:
            country: Country name or code (e.g., 'sri_lanka' or 'LKA', default: 'sri_lanka')
            start_year: Start year for historical data
            end_year: End year for historical data
        """
        # Handle both country names and codes
        country_lower = country.lower()
        if country_lower in COUNTRIES:
            self.country = country_lower
            self.country_code = COUNTRIES[country_lower]
        else:
            # Assume it's a country code (e.g., 'LKA')
            self.country = country
            self.country_code = country
        self.start_year = start_year
        self.end_year = end_year

        # Initialize clients
        self.wb_client = WorldBankClient(start_year, end_year)
        self.cbsl_client = CBSLClient()

        self.data_cache = {}
        logger.info(f"✓ DataManager initialized for {self.country_code}")

    def fetch_world_bank(self, indicators: Optional[Dict] = None) -> pd.DataFrame:
        """
        Fetch World Bank indicators

        Args:
            indicators: Dictionary of indicators (defaults to WORLD_BANK_INDICATORS)

        Returns:
            DataFrame with World Bank data
        """
        if indicators is None:
            indicators = WORLD_BANK_INDICATORS

        logger.info(f"Fetching {len(indicators)} World Bank indicators...")

        try:
            df = self.wb_client.fetch_multiple(self.country_code, indicators)
            self.data_cache['world_bank'] = df
            logger.info(f"✓ World Bank data cached ({df.shape[0]} rows, {df.shape[1]} columns)")
            return df
        except Exception as e:
            logger.error(f"✗ Failed to fetch World Bank data: {str(e)}")
            return pd.DataFrame()

    def fetch_alternative_sources(self) -> pd.DataFrame:
        """
        Fetch alternative indicators (tourism, remittances, etc.)

        Returns:
            DataFrame with alternative indicators
        """
        logger.info(f"Fetching {len(ALTERNATIVE_INDICATORS)} alternative indicators...")

        try:
            df = self.wb_client.fetch_multiple(self.country_code, ALTERNATIVE_INDICATORS)
            self.data_cache['alternative'] = df
            logger.info(f"✓ Alternative data cached ({df.shape[0]} rows, {df.shape[1]} columns)")
            return df
        except Exception as e:
            logger.error(f"✗ Failed to fetch alternative data: {str(e)}")
            return pd.DataFrame()

    def fetch_cbsl(self) -> pd.DataFrame:
        """
        Fetch CBSL indicators (monetary, financial)

        Returns:
            DataFrame with CBSL data (monthly resampled to annual)
        """
        logger.info("Fetching CBSL indicators...")

        try:
            df = self.cbsl_client.fetch_all()

            # Resample monthly data to annual (end-of-year) for consistency with WB
            df_annual = df.resample('YE').last()

            # Clean index
            df_annual.index = pd.to_datetime(df_annual.index.year, format='%Y')

            self.data_cache['cbsl'] = df_annual
            logger.info(f"✓ CBSL data cached ({df_annual.shape[0]} rows, {df_annual.shape[1]} columns)")
            return df_annual
        except Exception as e:
            logger.error(f"✗ Failed to fetch CBSL data: {str(e)}")
            return pd.DataFrame()

    def fetch_all(self, include_world_bank: bool = True,
                  include_alternative: bool = True,
                  include_cbsl: bool = True) -> pd.DataFrame:
        """
        Fetch all available data from all sources and merge

        Args:
            include_world_bank: Include World Bank indicators
            include_alternative: Include alternative sources (tourism, remittances)
            include_cbsl: Include CBSL monetary/financial indicators

        Returns:
            Merged DataFrame with all indicators
        """
        frames = []

        if include_world_bank:
            df_wb = self.fetch_world_bank()
            if not df_wb.empty:
                frames.append(df_wb)

        if include_alternative:
            df_alt = self.fetch_alternative_sources()
            if not df_alt.empty:
                frames.append(df_alt)

        if include_cbsl:
            df_cbsl = self.fetch_cbsl()
            if not df_cbsl.empty:
                frames.append(df_cbsl)

        if not frames:
            logger.error("✗ No data could be fetched from any source")
            return pd.DataFrame()

        # Merge all sources on index (date)
        df_merged = pd.concat(frames, axis=1)
        df_merged = df_merged.sort_index()

        logger.info(f"✓ Merged data from all sources: {df_merged.shape[0]} rows, {df_merged.shape[1]} columns")
        logger.info(f"Indicators: {list(df_merged.columns)}")

        return df_merged

    def get_summary(self) -> Dict:
        """
        Get summary statistics of all fetched data

        Returns:
            Dictionary with summary statistics
        """
        summary = {
            'country': self.country_code,
            'data_sources': list(self.data_cache.keys()),
            'total_rows': 0,
            'total_columns': 0,
            'indicators': [],
            'date_range': None
        }

        all_dates = []
        for source, df in self.data_cache.items():
            if df is not None and not df.empty:
                summary['total_rows'] = max(summary['total_rows'], len(df))
                summary['total_columns'] += len(df.columns)
                summary['indicators'].extend(df.columns.tolist())
                all_dates.extend(df.index.tolist())

        if all_dates:
            all_dates = pd.Series(all_dates)
            summary['date_range'] = f"{all_dates.min().year} - {all_dates.max().year}"

        return summary


# Example usage & testing
if __name__ == "__main__":
    print("\n" + "="*70)
    print("PHASE 1A: DATA ENRICHMENT - COMPREHENSIVE DATA FETCHING")
    print("="*70)

    # Initialize manager
    manager = DataManager(country="Sri Lanka", start_year=2015)

    # Fetch all data
    print("\n📊 Fetching comprehensive economic data...\n")
    df_all = manager.fetch_all()

    # Display summary
    print("\n" + "="*70)
    print("DATA SUMMARY")
    print("="*70)
    summary = manager.get_summary()
    print(f"Country: {summary['country']}")
    print(f"Date Range: {summary['date_range']}")
    print(f"Total Rows: {summary['total_rows']}")
    print(f"Total Columns/Indicators: {summary['total_columns']}")
    print(f"Data Sources: {', '.join(summary['data_sources'])}")

    print("\n" + "="*70)
    print("INDICATOR LIST")
    print("="*70)
    for i, indicator in enumerate(summary['indicators'], 1):
        print(f"{i:2d}. {indicator}")

    print("\n" + "="*70)
    print("LATEST DATA (Most Recent Year)")
    print("="*70)
    print(df_all.tail())

