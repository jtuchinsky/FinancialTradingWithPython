# 1. What is financial trading

Summary of the DataCamp exercise
[*What is financial trading*](https://campus.datacamp.com/courses/financial-trading-in-python/trading-basics-1?ex=1)
(instructor: Chelsea Yang).

## Definition

Financial trading is the **purchase and sale of financial securities**. Traders work across many
instruments: equities, bonds, forex, commodities, and cryptocurrencies.

## Why people trade

- **Profit** by taking calculated risk:
  - **Long position** — buy low, sell high.
  - **Short position** — sell a borrowed asset high, then buy it back lower.
- **Institutional traders** (hedge funds, investment banks) also trade to hedge risk, provide market
  liquidity, or rebalance portfolios.

## Trading vs. investing

| | Trading | Investing |
|---|---|---|
| Time horizon | Days to months | Years to decades |
| Focus | Short-term trends & volatility | Fundamentals & macroeconomics |
| Positions | Both long **and** short | Typically long only |

## Technical analysis

This course focuses on **technical trading**: studying historical price patterns and acting on
strategies built from indicators, signals, and predetermined rules.

## Python tools used in the course

- **pandas** — data manipulation (e.g. `read_csv`, `parse_dates`).
- **matplotlib** — visualization.
- **plotly** — interactive charts via `plotly.graph_objects` (e.g. candlestick charts).

## Data visualization

- **Line charts** for time-series price data.
- **Candlestick charts** showing the open, high, low, and close (OHLC) prices within each period.