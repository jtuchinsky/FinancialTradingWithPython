"""Generate a synthetic `eurusd_4h` DataFrame matching the description in
`eurusd_4h.txt` (Topic 1 folder).

The real DataCamp exercise ("Resample the data", Chapter 1 ex 6) preloads a
4-hour EUR/USD OHLC frame we don't have. This reproduces its *shape and summary
statistics* — 6094 rows at 4h frequency from 2016-01-04, columns Open/Close/High/Low,
mean ~1.135, std ~0.045, range ~1.037-1.256 — so the exercise can be run locally.

Values are synthetic (a seeded mean-reverting random walk), not the real rates.

    from eurusd_4h import make_eurusd_4h
    eurusd_4h = make_eurusd_4h()
"""

import numpy as np
import pandas as pd

# Target summary stats (from eurusd_4h.txt describe())
N_ROWS = 6094
START = "2016-01-04 00:00:00"
FREQ = "4h"
MEAN, STD = 1.135, 0.045
LO, HI = 1.037, 1.255


def make_eurusd_4h(seed: int = 0) -> pd.DataFrame:
    """Return a synthetic 4-hour EUR/USD OHLC DataFrame (DatetimeIndex 'Date')."""
    rng = np.random.default_rng(seed)

    # 1. Mean-reverting (Ornstein-Uhlenbeck) mid path for realistic autocorrelation
    kappa, sigma = 0.02, 0.01
    x = np.empty(N_ROWS)
    x[0] = MEAN
    for t in range(1, N_ROWS):
        x[t] = x[t - 1] + kappa * (MEAN - x[t - 1]) + sigma * rng.standard_normal()

    # 2. Affine-normalize so mean/std match the target exactly, then clip to range
    close = MEAN + STD * (x - x.mean()) / x.std()
    close = np.clip(close, LO, HI)

    # 3. Derive the other columns
    #    Open = previous close (continuous FX); first bar seeded near close[0]
    open_ = np.empty(N_ROWS)
    open_[0] = close[0] + 0.001
    open_[1:] = close[:-1]

    #    Per the source stats, "High" sits slightly below and "Low" slightly above
    #    the close (mean 1.133 vs 1.136) with per-bar noise.
    high = close - 0.002 + rng.normal(0, 0.006, N_ROWS)
    low = close + 0.001 + rng.normal(0, 0.006, N_ROWS)

    idx = pd.date_range(start=START, periods=N_ROWS, freq=FREQ, name="Date")
    df = pd.DataFrame(
        {"Open": open_, "Close": close, "High": high, "Low": low},
        index=idx,
    ).round(3)
    return df


if __name__ == "__main__":
    eurusd_4h = make_eurusd_4h()

    print("print(eurusd_4h.columns)")
    print(eurusd_4h.columns, "\n")

    print("print(eurusd_4h.describe())")
    print(eurusd_4h.describe().round(3), "\n")

    print("print(eurusd_4h.shape)")
    print(eurusd_4h.shape, "\n")

    print("print(eurusd_4h.head(2))")
    print(eurusd_4h.head(2))
