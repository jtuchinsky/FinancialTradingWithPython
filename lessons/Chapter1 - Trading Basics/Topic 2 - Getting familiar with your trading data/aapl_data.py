"""Generate a synthetic `aapl_data` DataFrame matching the description in
`aapl.txt` (Topic 1 folder).

The real DataCamp exercise ("Calculate and plot SMAs", Chapter 1 ex 8) preloads
a daily AAPL OHLCV frame we don't have. This reproduces its *shape and summary
statistics* — 503 business days from 2018-01-02, columns
Open/High/Low/Close/Adj Close/Volume, Close mean ~49.7 / range ~35.6-73.4
(right-skewed), Adj Close a touch below Close, Volume ~1.24e8 — so the exercise
can be run locally.

The Close series is built by **rank-mapping** an autocorrelated random path onto
the target quantiles, so its min/quartiles/median/max match closely. Values are
synthetic, not the real prices.

    from aapl_data import make_aapl_data
    aapl_data = make_aapl_data()
"""

import numpy as np
import pandas as pd

N_ROWS = 503
START = "2018-01-02"

# Target Close quantiles (prob, value). The 0/25/50/75/100 points come from
# aapl.txt describe(); the 90/96/99.5 knots shape the upper tail so the mean and
# every quartile land on target. (std runs a little high, ~8.7 vs 7.5 — the target
# combines a low std with a wide, skewed range, which a smooth quantile map can't
# fully reproduce; the real series was concentrated with a brief late spike.)
CLOSE_QUANTILES = [
    (0.000, 35.55), (0.250, 43.88), (0.500, 48.15), (0.750, 53.87),
    (0.900, 62.90), (0.960, 67.60), (0.995, 72.30), (1.000, 73.41),
]

# Volume: right-skewed lognormal, clipped to the observed range
VOL_MEDIAN, VOL_SIGMA = 1.14e8, 0.43
VOL_LO, VOL_HI = 4.545e7, 3.85e8


def make_aapl_data(seed: int = 0) -> pd.DataFrame:
    """Return a synthetic daily AAPL OHLCV DataFrame (business-day 'Date' index)."""
    rng = np.random.default_rng(seed)
    idx = pd.bdate_range(start=START, periods=N_ROWS, name="Date")

    # 1. Autocorrelated path -> ranks -> map onto the target Close quantiles
    x = np.empty(N_ROWS)
    x[0] = 0.0
    for t in range(1, N_ROWS):
        x[t] = 0.98 * x[t - 1] + rng.standard_normal()
    u = (x.argsort().argsort() + 0.5) / N_ROWS      # ranks in (0, 1)
    qx = [p for p, _ in CLOSE_QUANTILES]
    qy = [v for _, v in CLOSE_QUANTILES]
    close = np.interp(u, qx, qy)

    # 2. Open ~ previous close with a small overnight gap
    open_ = np.empty(N_ROWS)
    open_[0] = close[0]
    open_[1:] = close[:-1] * (1 + rng.normal(0, 0.003, N_ROWS - 1))

    # 3. High/Low bracket max/min(Open, Close) with a positive intraday wick
    high = np.maximum(open_, close) + np.abs(rng.normal(0, 0.0035, N_ROWS)) * close
    low = np.minimum(open_, close) - np.abs(rng.normal(0, 0.0035, N_ROWS)) * close

    # 4. Adj Close: dividend-adjusted, factor drifts up over the period (mean ~0.972)
    adj_close = close * np.linspace(0.969, 0.987, N_ROWS)

    # 5. Volume: right-skewed lognormal, clipped to the observed range
    volume = np.clip(rng.lognormal(np.log(VOL_MEDIAN), VOL_SIGMA, N_ROWS), VOL_LO, VOL_HI)

    return pd.DataFrame(
        {
            "Open": open_.round(2),
            "High": high.round(2),
            "Low": low.round(2),
            "Close": close.round(2),
            "Adj Close": adj_close.round(2),
            "Volume": volume.astype("int64"),
        },
        index=idx,
    )


if __name__ == "__main__":
    aapl_data = make_aapl_data()

    print("print(aapl_data.columns)")
    print(aapl_data.columns, "\n")

    print("print(aapl_data.describe())")
    with pd.option_context("display.float_format", lambda v: f"{v:.3f}"):
        print(aapl_data.describe(), "\n")

    print("print(aapl_data.shape)")
    print(aapl_data.shape, "\n")

    print("print(aapl_data.head(2))")
    print(aapl_data.head(2))
