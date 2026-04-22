import numpy as np
import pandas as pd

def compute_cross_correlation(x: pd.Series,
                              y: pd.Series,
                              max_lag: int = 36):
    """
    Returns correlation for lags:
    negative lag → y leads x
    positive lag → x leads y
    """

    results = []

    x = x.dropna()
    y = y.dropna()

    min_len = min(len(x), len(y))
    x = x[-min_len:]
    y = y[-min_len:]

    for lag in range(-max_lag, max_lag + 1):

        if lag < 0:
            corr = np.corrcoef(x[:lag], y[-lag:])[0, 1]

        elif lag > 0:
            corr = np.corrcoef(x[lag:], y[:-lag])[0, 1]

        else:
            corr = np.corrcoef(x, y)[0, 1]

        results.append({
            "lag": lag,
            "correlation": corr
        })

    return pd.DataFrame(results)