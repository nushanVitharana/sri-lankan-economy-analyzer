from __future__ import annotations

import numpy as np
import pandas as pd


EPSILON = 1e-9


def safe_pct_change(series: pd.Series, periods: int = 1) -> pd.Series:
    cleaned = series.replace([np.inf, -np.inf], np.nan)
    return cleaned.pct_change(periods=periods) * 100


def bounded_zscore(series: pd.Series) -> pd.Series:
    cleaned = series.replace([np.inf, -np.inf], np.nan)
    std = cleaned.std(ddof=0)
    if std is None or std == 0 or np.isnan(std):
        return pd.Series(0.0, index=cleaned.index)
    return ((cleaned - cleaned.mean()) / std).clip(-3, 3)


def normalized_score(series: pd.Series, invert: bool = False) -> pd.Series:
    score = bounded_zscore(series)
    if invert:
        score = -score
    return score


def add_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    enriched = df.copy()

    if {"exports_usd", "imports_usd"}.issubset(enriched.columns):
        enriched["trade_gap_usd"] = enriched["exports_usd"] - enriched["imports_usd"]

    if {"reserves", "imports_usd"}.issubset(enriched.columns):
        annual_imports = enriched["imports_usd"].replace(0, np.nan)
        enriched["import_cover_months"] = (enriched["reserves"] / annual_imports) * 12

    if "reserves" in enriched.columns:
        enriched["reserves_yoy_change"] = safe_pct_change(enriched["reserves"])

    if "exchange_rate_usd" in enriched.columns:
        enriched["fx_depreciation_yoy"] = safe_pct_change(enriched["exchange_rate_usd"])

    if "money_supply_m2" in enriched.columns:
        enriched["money_supply_growth_yoy"] = safe_pct_change(enriched["money_supply_m2"])

    if "credit_private_sector" in enriched.columns:
        enriched["credit_growth_yoy"] = safe_pct_change(enriched["credit_private_sector"])

    if "inflation" in enriched.columns:
        enriched["inflation_acceleration"] = enriched["inflation"].diff()

    if {"expense_pct_gdp", "revenue_pct_gdp"}.issubset(enriched.columns):
        enriched["fiscal_gap_pct_gdp"] = enriched["expense_pct_gdp"] - enriched["revenue_pct_gdp"]

    if {"debt_service_pct_exports", "exports_pct_gdp"}.issubset(enriched.columns):
        enriched["debt_service_trade_burden"] = (
            enriched["debt_service_pct_exports"] * enriched["exports_pct_gdp"] / 100
        )

    if {"food_inflation_proxy", "inflation"}.issubset(enriched.columns):
        enriched["food_inflation_gap"] = enriched["food_inflation_proxy"] - enriched["inflation"]

    return enriched


def add_composite_indices(df: pd.DataFrame) -> pd.DataFrame:
    enriched = df.copy()

    external_components = []
    if "import_cover_months" in enriched.columns:
        external_components.append(normalized_score(enriched["import_cover_months"], invert=True))
    if "current_account_pct_gdp" in enriched.columns:
        external_components.append(normalized_score(enriched["current_account_pct_gdp"], invert=True))
    if "fx_depreciation_yoy" in enriched.columns:
        external_components.append(normalized_score(enriched["fx_depreciation_yoy"]))
    if "short_term_debt_pct_reserves" in enriched.columns:
        external_components.append(normalized_score(enriched["short_term_debt_pct_reserves"]))

    fiscal_components = []
    if "debt" in enriched.columns:
        fiscal_components.append(normalized_score(enriched["debt"]))
    if "fiscal_gap_pct_gdp" in enriched.columns:
        fiscal_components.append(normalized_score(enriched["fiscal_gap_pct_gdp"]))
    if "debt_service_pct_exports" in enriched.columns:
        fiscal_components.append(normalized_score(enriched["debt_service_pct_exports"]))

    monetary_components = []
    if "inflation" in enriched.columns:
        monetary_components.append(normalized_score(enriched["inflation"]))
    if "food_inflation_gap" in enriched.columns:
        monetary_components.append(normalized_score(enriched["food_inflation_gap"]))
    if "money_supply_growth_yoy" in enriched.columns:
        monetary_components.append(normalized_score(enriched["money_supply_growth_yoy"]))
    if "fx_depreciation_yoy" in enriched.columns:
        monetary_components.append(normalized_score(enriched["fx_depreciation_yoy"]))

    household_components = []
    if "food_inflation_proxy" in enriched.columns:
        household_components.append(normalized_score(enriched["food_inflation_proxy"]))
    if "unemployment_rate" in enriched.columns:
        household_components.append(normalized_score(enriched["unemployment_rate"]))
    if "poverty_headcount" in enriched.columns:
        household_components.append(normalized_score(enriched["poverty_headcount"]))

    for name, components in {
        "external_vulnerability_index": external_components,
        "fiscal_stress_index": fiscal_components,
        "monetary_pressure_index": monetary_components,
        "household_stress_index": household_components,
    }.items():
        if components:
            enriched[name] = pd.concat(components, axis=1).mean(axis=1) * 10 + 50

    index_columns = [
        col for col in enriched.columns
        if col.endswith("_index")
    ]
    if index_columns:
        enriched["macro_stress_index"] = enriched[index_columns].mean(axis=1)
        enriched["risk_regime"] = enriched["macro_stress_index"].apply(classify_risk_regime)

    return enriched


def classify_risk_regime(value: float) -> str:
    if pd.isna(value):
        return "Unknown"
    if value >= 65:
        return "Crisis"
    if value >= 57:
        return "Stress"
    if value >= 50:
        return "Watch"
    return "Stable"


def enrich_dataset(df: pd.DataFrame) -> pd.DataFrame:
    enriched = add_derived_features(df)
    enriched = add_composite_indices(enriched)
    enriched = enriched.replace([np.inf, -np.inf], np.nan)
    return enriched


def build_risk_summary(df: pd.DataFrame) -> dict:
    if df.empty:
        return {}

    latest = df.ffill().iloc[-1]
    previous = df.ffill().iloc[-2] if len(df) > 1 else latest

    def trend(col: str) -> str:
        if col not in df.columns or pd.isna(latest.get(col)) or pd.isna(previous.get(col)):
            return "flat"
        if latest[col] > previous[col]:
            return "rising"
        if latest[col] < previous[col]:
            return "easing"
        return "flat"

    summary = {
        "risk_regime": latest.get("risk_regime", "Unknown"),
        "macro_stress_index": round(float(latest.get("macro_stress_index", np.nan)), 1)
        if pd.notna(latest.get("macro_stress_index", np.nan)) else None,
        "external_vulnerability_index": round(float(latest.get("external_vulnerability_index", np.nan)), 1)
        if pd.notna(latest.get("external_vulnerability_index", np.nan)) else None,
        "fiscal_stress_index": round(float(latest.get("fiscal_stress_index", np.nan)), 1)
        if pd.notna(latest.get("fiscal_stress_index", np.nan)) else None,
        "monetary_pressure_index": round(float(latest.get("monetary_pressure_index", np.nan)), 1)
        if pd.notna(latest.get("monetary_pressure_index", np.nan)) else None,
        "household_stress_index": round(float(latest.get("household_stress_index", np.nan)), 1)
        if pd.notna(latest.get("household_stress_index", np.nan)) else None,
        "import_cover_months": round(float(latest.get("import_cover_months", np.nan)), 2)
        if pd.notna(latest.get("import_cover_months", np.nan)) else None,
        "fx_depreciation_yoy": round(float(latest.get("fx_depreciation_yoy", np.nan)), 2)
        if pd.notna(latest.get("fx_depreciation_yoy", np.nan)) else None,
        "inflation": round(float(latest.get("inflation", np.nan)), 2)
        if pd.notna(latest.get("inflation", np.nan)) else None,
        "top_story": infer_top_story(latest),
        "trends": {
            "external": trend("external_vulnerability_index"),
            "fiscal": trend("fiscal_stress_index"),
            "monetary": trend("monetary_pressure_index"),
            "households": trend("household_stress_index"),
        },
    }
    return summary


def infer_top_story(latest: pd.Series) -> str:
    index_cols = {
        "external_vulnerability_index": "External pressure remains the dominant risk.",
        "fiscal_stress_index": "Fiscal conditions are driving the stress profile.",
        "monetary_pressure_index": "Inflation and monetary pressure are leading the risk picture.",
        "household_stress_index": "Household cost pressure is still elevated.",
    }
    available = {col: latest.get(col) for col in index_cols if pd.notna(latest.get(col))}
    if not available:
        return "Not enough enriched data for a conclusion yet."
    top_col = max(available, key=available.get)
    return index_cols[top_col]
