# 4. Plot a candlestick chart

Summary of the DataCamp exercise
[*Plot a candlestick chart*](https://campus.datacamp.com/courses/financial-trading-in-python/trading-basics-1?ex=4).

**Exercise type:** Coding.

## Context

Candlestick charts are a staple of technical analysis: each candle packs four prices —
**open, high, low, and close (OHLC)** — into a single visual element for one period. Here you build
one from the pre-loaded Bitcoin price data using **plotly**.

## Available tools

- `bitcoin_data` — pre-loaded DataFrame of price information (indexed by date).
- `plotly.graph_objects` imported as `go`.

## Tasks

1. Construct a **candlestick object** from the OHLC columns.
2. Build a **figure** containing the candlestick.
3. **Render** the chart.

## Representative solution

```python
# 1. Define the candlestick data
candlestick = go.Candlestick(
    x=bitcoin_data.index,
    open=bitcoin_data['open'],
    high=bitcoin_data['high'],
    low=bitcoin_data['low'],
    close=bitcoin_data['close'])

# 2. Create a candlestick figure
fig = go.Figure(data=[candlestick])
fig.update_layout(title='Bitcoin prices')

# 3. Show the plot
fig.show()
```

## Key takeaways

- `go.Candlestick` needs `x` plus the four OHLC series (`open`, `high`, `low`, `close`).
- A single candle conveys far more than a line point: body = open→close, wicks = high/low, so the
  chart shows both direction and intraperiod volatility.
- `plotly` candlesticks are interactive (zoom, hover), which suits exploring price action.

> Note: exact column/variable names come from DataCamp's interactive editor; the code above is a
> faithful reconstruction of the expected solution.