#!/usr/bin/env python3
"""
Sri Lankan Economy Analyzer - Main Program
==========================================

This program executes the complete economic analysis pipeline:
1. Data Ingestion (World Bank API)
2. Data Processing & Cleaning
3. Cross-Correlation Analysis
4. Anomaly Detection
5. Crisis Detection
6. Results Visualization & Export

Author: Sri Lankan Economy Analyzer Team
Date: April 2026
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Import all project modules
from src.ingestion.world_bank import WorldBankClient
from src.ingestion.config import WORLD_BANK_INDICATORS, COUNTRIES
from src.processing.pipeline import build_master_dataset, save_master_dataset
from src.models.cross_correlation import compute_cross_correlation
from src.models.lag_detector import find_best_lag, interpret_lag
from src.models.anomaly_detection import detect_anomalies
from src.models.crisis_detection import detect_crisis_point, normalize_to_crisis
from src.dashboard.data_loader import DashboardData


def main():
    """
    Execute the complete Sri Lankan Economy Analysis pipeline
    """
    print("=" * 60)
    print("🇱🇰 SRI LANKAN ECONOMY ANALYZER 🇱🇰")
    print("=" * 60)
    print(f"Execution started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # ===============================
    # 1. DATA INGESTION
    # ===============================
    print("📊 PHASE 1: Data Ingestion")
    print("-" * 30)

    print("Fetching World Bank data for Sri Lanka...")
    client = WorldBankClient()

    # Get raw data
    df_raw = client.fetch_multiple(
        country=COUNTRIES["sri_lanka"],
        indicators=WORLD_BANK_INDICATORS
    )

    print(f"✓ Retrieved {len(df_raw)} rows of raw data")
    print(f"✓ Columns: {', '.join(df_raw.columns.tolist())}")
    print(f"✓ Date range: {df_raw.index.min()} to {df_raw.index.max()}")
    print()

    # ===============================
    # 2. DATA PROCESSING
    # ===============================
    print("🔧 PHASE 2: Data Processing")
    print("-" * 30)

    # Split into series for processing
    series_dict = {col: df_raw[[col]] for col in df_raw.columns}

    # Build master dataset
    print("Processing data through cleaning pipeline...")
    master_df = build_master_dataset(series_dict)

    print(f"✓ Processed dataset: {len(master_df)} rows")
    print(f"✓ Date range: {master_df.index.min()} to {master_df.index.max()}")
    print()

    # Save processed data
    output_path = "data/processed/master_latest.csv"
    save_master_dataset(master_df, output_path)
    print(f"✓ Saved processed data to: {output_path}")
    print()

    # ===============================
    # 3. CROSS-CORRELATION ANALYSIS
    # ===============================
    print("📈 PHASE 3: Cross-Correlation Analysis")
    print("-" * 40)

    # Analyze relationships between key indicators
    analysis_pairs = [
        ("reserves", "inflation"),
        ("reserves", "debt"),
        ("inflation", "debt")
    ]

    correlation_results = {}

    for var1, var2 in analysis_pairs:
        print(f"Analyzing {var1} ↔ {var2}...")

        # Compute cross-correlation
        corr_df = compute_cross_correlation(master_df[var1], master_df[var2])
        best_lag = find_best_lag(corr_df)
        interpretation = interpret_lag(best_lag, var1, var2)

        correlation_results[f"{var1}_vs_{var2}"] = {
            "correlation_df": corr_df,
            "best_lag": best_lag,
            "interpretation": interpretation
        }

        print(f"  → {interpretation}")
        print()

    # ===============================
    # 4. ANOMALY DETECTION
    # ===============================
    print("🔍 PHASE 4: Anomaly Detection")
    print("-" * 30)

    anomaly_results = {}

    for col in master_df.columns:
        print(f"Detecting anomalies in {col}...")
        anomalies = detect_anomalies(master_df[col])

        anomaly_results[col] = anomalies

        if len(anomalies) > 0:
            print(f"  → Found {len(anomalies)} anomalies")
            print(f"  → Most recent: {anomalies.index[-1].strftime('%Y-%m-%d')}")
        else:
            print("  → No significant anomalies detected")
        print()

    # ===============================
    # 5. CRISIS DETECTION
    # ===============================
    print("⚠️  PHASE 5: Crisis Detection")
    print("-" * 30)

    crisis_results = {}

    for col in master_df.columns:
        print(f"Detecting crisis points in {col}...")
        crisis_date = detect_crisis_point(master_df[col])

        crisis_results[col] = crisis_date

        print(f"  → Crisis point: {crisis_date.strftime('%Y-%m-%d')}")
        print(f"  → Value: {master_df.loc[crisis_date, col]:.2f}")
        print()

    # ===============================
    # 6. RESULTS SUMMARY
    # ===============================
    print("📋 PHASE 6: Results Summary")
    print("-" * 30)

    print("DATASET OVERVIEW:")
    print(f"• Total observations: {len(master_df)}")
    print(f"• Time period: {master_df.index.min().year} - {master_df.index.max().year}")
    print(f"• Variables: {', '.join(master_df.columns.tolist())}")
    print()

    print("KEY ECONOMIC INSIGHTS:")
    for pair_key, result in correlation_results.items():
        var1, var2 = pair_key.split("_vs_")
        print(f"• {var1.title()} vs {var2.title()}: {result['interpretation']}")

    print()
    print("ANOMALY SUMMARY:")
    for var, anomalies in anomaly_results.items():
        print(f"• {var.title()}: {len(anomalies)} anomalies detected")

    print()
    print("CRISIS TIMELINE:")
    for var, crisis_date in crisis_results.items():
        print(f"• {var.title()} crisis: {crisis_date.strftime('%B %Y')}")

    print()

    # ===============================
    # 7. EXPORT RESULTS
    # ===============================
    print("💾 PHASE 7: Export Results")
    print("-" * 30)

    # Export correlation results
    for pair_key, result in correlation_results.items():
        filename = f"data/processed/correlation_{pair_key}.csv"
        result["correlation_df"].to_csv(filename)
        print(f"✓ Exported {pair_key} correlations to {filename}")

    # Export anomaly results
    anomaly_summary = pd.DataFrame({
        var: {"count": len(anomalies), "dates": anomalies.index.tolist() if len(anomalies) > 0 else []}
        for var, anomalies in anomaly_results.items()
    }).T
    anomaly_summary.to_csv("data/processed/anomaly_summary.csv")
    print("✓ Exported anomaly summary to data/processed/anomaly_summary.csv")

    # Export crisis results
    crisis_summary = pd.DataFrame({
        var: {"crisis_date": crisis_date, "crisis_value": master_df.loc[crisis_date, var]}
        for var, crisis_date in crisis_results.items()
    }).T
    crisis_summary.to_csv("data/processed/crisis_summary.csv")
    print("✓ Exported crisis summary to data/processed/crisis_summary.csv")

    print()

    # ===============================
    # 8. FINAL REPORT
    # ===============================
    print("🎉 ANALYSIS COMPLETE!")
    print("=" * 60)

    execution_time = datetime.now()
    print(f"Completed at: {execution_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print("📁 Output files saved to: data/processed/")
    print("📊 Dashboard data ready for visualization")
    print("🔬 Analysis results exported for further study")
    print()
    print("Thank you for using Sri Lankan Economy Analyzer! 🇱🇰")
    print("=" * 60)


if __name__ == "__main__":
    main()
