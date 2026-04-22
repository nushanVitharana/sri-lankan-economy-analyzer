import pandas as pd
import numpy as np
import pytest
import tempfile
import os

from src.dashboard.data_loader import DashboardData
from src.models.cross_correlation import compute_cross_correlation
from src.models.lag_detector import find_best_lag, interpret_lag


# ----------------------------
# Mock Dataset (controlled test)
# ----------------------------
def create_mock_data():
    dates = pd.date_range(start="2020-01-01", periods=100, freq="ME")

    # Create synthetic leading relationship
    reserves = np.linspace(100, 50, 100)  # declining
    fx_rate = np.roll(reserves, 5) * -1   # lagged inverse relation

    df = pd.DataFrame({
        "reserves": reserves,
        "fx_rate": fx_rate,
        "inflation": np.random.normal(5, 1, 100)
    }, index=dates)

    return df


# ----------------------------
# Test Data Loader
# ----------------------------
def test_data_loader_basic(tmp_path):
    df = create_mock_data()

    file_path = tmp_path / "test.csv"
    df.to_csv(file_path)

    loader = DashboardData(path=str(file_path))

    assert not loader.df.empty
    assert "reserves" in loader.get_columns()


# ----------------------------
# Test Cross Correlation
# ----------------------------
def test_cross_correlation():
    df = create_mock_data()

    corr_df = compute_cross_correlation(
        df["reserves"],
        df["fx_rate"],
        max_lag=10
    )

    assert not corr_df.empty
    assert "lag" in corr_df.columns
    assert "correlation" in corr_df.columns


# ----------------------------
# Test Lag Detection
# ----------------------------
def test_lag_detection():
    df = create_mock_data()

    corr_df = compute_cross_correlation(
        df["reserves"],
        df["fx_rate"],
        max_lag=10
    )

    best = find_best_lag(corr_df)

    assert isinstance(best["lag"], int)
    assert isinstance(best["correlation"], float)


# ----------------------------
# Test Interpretation Output
# ----------------------------
def test_interpretation():
    result = {"lag": 5, "correlation": 0.8}

    text = interpret_lag(result, "reserves", "fx_rate")

    assert "reserves leads fx_rate" in text
    assert "5" in text


# ----------------------------
# Test Full Pipeline Logic
# ----------------------------
def test_full_signal_pipeline():
    df = create_mock_data()

    corr_df = compute_cross_correlation(
        df["reserves"],
        df["fx_rate"]
    )

    best = find_best_lag(corr_df)
    text = interpret_lag(best, "reserves", "fx_rate")

    assert isinstance(text, str)
    assert len(text) > 0