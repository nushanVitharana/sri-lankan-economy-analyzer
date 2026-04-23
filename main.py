#!/usr/bin/env python3
"""
Sri Lankan Economy Analyzer - Main Program
"""

from datetime import datetime
import os

import pandas as pd

from src.ingestion.data_manager import DataManager
from src.models.anomaly_detection import detect_anomalies
from src.models.crisis_detection import detect_crisis_point
from src.models.cross_correlation import compute_cross_correlation
from src.models.lag_detector import find_best_lag, interpret_lag


def main():
    print("=" * 70)
    print("SRI LANKAN ECONOMY ANALYZER")
    print("=" * 70)
    print(f"Execution started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    manager = DataManager(country="sri_lanka", start_year=2010, end_year=2025)
    df_all = manager.fetch_all()
    risk_summary = manager.get_risk_summary()

    os.makedirs("data/processed", exist_ok=True)
    df_all.to_csv("data/processed/master_latest.csv")

    print("DATASET OVERVIEW")
    print("-" * 30)
    print(f"Observations: {len(df_all)}")
    print(f"Variables: {len(df_all.columns)}")
    print(f"Date range: {df_all.index.min().year} - {df_all.index.max().year}")
    print(f"Risk regime: {risk_summary.get('risk_regime', 'Unknown')}")
    print(f"Top story: {risk_summary.get('top_story', 'n/a')}")
    print()

    analysis_pairs = [
        ("external_vulnerability_index", "monetary_pressure_index"),
        ("reserves", "inflation"),
        ("exchange_rate_usd", "inflation"),
        ("debt", "fiscal_stress_index"),
    ]

    print("SIGNAL ANALYSIS")
    print("-" * 30)
    correlation_results = {}
    for var1, var2 in analysis_pairs:
        if var1 not in df_all.columns or var2 not in df_all.columns:
            continue
        corr_df = compute_cross_correlation(df_all[var1], df_all[var2], max_lag=6)
        best_lag = find_best_lag(corr_df)
        interpretation = interpret_lag(best_lag, var1, var2)
        correlation_results[f"{var1}_vs_{var2}"] = {
            "correlation_df": corr_df,
            "best_lag": best_lag,
            "interpretation": interpretation,
        }
        print(f"{var1} vs {var2}: {interpretation}")
    print()

    anomaly_targets = [
        col for col in [
            "macro_stress_index",
            "external_vulnerability_index",
            "fiscal_stress_index",
            "monetary_pressure_index",
            "household_stress_index",
        ] if col in df_all.columns
    ]
    anomaly_summary = {}
    crisis_summary = {}

    print("RISK EXTREMES")
    print("-" * 30)
    for col in anomaly_targets:
        anomalies = detect_anomalies(df_all[col].dropna())
        crisis_date = detect_crisis_point(df_all[col].dropna())
        anomaly_summary[col] = len(anomalies)
        crisis_summary[col] = crisis_date
        print(f"{col}: {len(anomalies)} anomalies, crisis point {crisis_date.strftime('%Y-%m-%d')}")
    print()

    for pair_key, result in correlation_results.items():
        result["correlation_df"].to_csv(f"data/processed/correlation_{pair_key}.csv", index=False)

    pd.DataFrame.from_dict(anomaly_summary, orient="index", columns=["count"]).to_csv(
        "data/processed/anomaly_summary.csv"
    )
    pd.DataFrame(
        {
            "crisis_date": {key: value for key, value in crisis_summary.items()},
        }
    ).to_csv("data/processed/crisis_summary.csv")
    pd.DataFrame([risk_summary]).to_csv("data/processed/risk_summary.csv", index=False)

    print("ANALYSIS COMPLETE")
    print("=" * 70)
    print("Saved enriched dataset and risk summaries to data/processed/")


if __name__ == "__main__":
    main()
