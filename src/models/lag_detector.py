def find_best_lag(corr_df):
    """
    Returns lag with highest absolute correlation
    """

    best_row = corr_df.iloc[corr_df["correlation"].abs().idxmax()]

    return {
        "lag": int(best_row["lag"]),
        "correlation": float(best_row["correlation"])
    }


def interpret_lag(result, x_name, y_name):
    lag = result["lag"]
    corr = result["correlation"]

    if lag > 0:
        relation = f"{x_name} leads {y_name}"
    elif lag < 0:
        relation = f"{y_name} leads {x_name}"
    else:
        relation = "no clear lead-lag relationship"

    return f"{relation} by {abs(lag)} months (r={corr:.2f})"