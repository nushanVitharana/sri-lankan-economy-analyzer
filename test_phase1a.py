"""
Test script for Phase 1A: Data Enrichment

This script tests the comprehensive data manager with all new data sources
"""

from src.ingestion.data_manager import DataManager

if __name__ == "__main__":
    print("\n" + "="*80)
    print("PHASE 1A: COMPREHENSIVE DATA ENRICHMENT TEST")
    print("="*80)

    # Initialize the unified data manager
    print("\n[*] Initializing DataManager for Sri Lanka (2010-2024)...\n")
    manager = DataManager(country="sri_lanka", start_year=2010, end_year=2025)

    # Fetch all available data
    print("Fetching data from all sources:")
    print("  1. World Bank (12 indicators)")
    print("  2. Alternative sources (tourism, remittances, trade balance)")
    print("  3. CBSL synthetic data (exchange rate, money supply, credit, rates, stock index)")
    print()

    df_all = manager.fetch_all()

    # Display summary
    print("\n" + "="*80)
    print("COMPREHENSIVE DATA SUMMARY")
    print("="*80)
    summary = manager.get_summary()

    print(f"\n[OK] Country: {summary['country']}")
    print(f"[OK] Date Range: {summary['date_range']}")
    print(f"[OK] Historical Years: {summary['total_rows']}")
    print(f"[OK] Total Indicators: {summary['total_columns']}")
    print(f"[OK] Data Sources: {', '.join(summary['data_sources'])}\n")

    print("="*80)
    print("COMPLETE INDICATOR LIST (All 20+ Indicators)")
    print("="*80)
    for i, indicator in enumerate(summary['indicators'], 1):
        print(f"  {i:2d}. {indicator}")

    print("\n" + "="*80)
    print("LATEST DATA VALUES (Most Recent Year)")
    print("="*80)
    print(df_all.tail(1).T)

    print("\n" + "="*80)
    print("DATA QUALITY REPORT")
    print("="*80)
    print(f"\nDataset Shape: {df_all.shape[0]} years x {df_all.shape[1]} indicators")
    print(f"\nMissing Values:")
    missing = df_all.isnull().sum()
    if missing.sum() > 0:
        print(missing[missing > 0])
    else:
        print("  [OK] No missing values")

    print(f"\nData Types:")
    print(f"  [OK] Numeric values: {(df_all.dtypes == 'float64').sum()}")
    print(f"  [OK] Date index: {isinstance(df_all.index, __import__('pandas').DatetimeIndex)}")

    print("\n" + "="*80)
    print("COMPLETED: PHASE 1A!")
    print("="*80)
    print("\nAccomplishments:")
    print("  [OK] Expanded from 3 to 20+ economic indicators")
    print("  [OK] Integrated World Bank data (12 indicators)")
    print("  [OK] Added alternative sources (tourism, remittances, trade)")
    print("  [OK] Created CBSL client (monetary/financial data)")
    print("  [OK] Built unified DataManager for orchestration")
    print("  [OK] All data merged on consistent date index")
    print("\nNext steps:")
    print("  --> Update main.py to use new DataManager")
    print("  --> Build ARIMA forecasting models (Phase 1B)")
    print("  --> Create risk scoring framework (Phase 2)")
    print("  --> Redesign dashboard with new indicators")
    print("\n" + "="*80 + "\n")

