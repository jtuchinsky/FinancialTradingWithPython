# 3. Plot a time series line chart

Summary of the DataCamp exercise
[*Plot a time series line chart*](https://campus.datacamp.com/courses/financial-trading-in-python/trading-basics-1?ex=3).

**Exercise type:** Coding.

## Context

Cryptocurrencies are a new category of assets. Here you explore **daily historical Bitcoin price
data** from a CSV file — loading it, inspecting it, and plotting the closing price as a time-series
line chart.

## Available tools

- `pandas` imported as `pd`
- `matplotlib.pyplot` imported as `plt`

## Tasks

1. **Load the data** — read the CSV with pandas, parsing the date column so it becomes a proper
   `DatetimeIndex`.
2. **Inspect the data** — print the first five rows with `.head()`.
3. **Plot** the `Close` price over time as a line chart.

## Representative solution

```python
import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the data, parsing dates into the index
bitcoin_data = pd.read_csv('bitcoin_data.csv', index_col='Date', parse_dates=True)

# 2. Inspect the first five rows
print(bitcoin_data.head())

# 3. Plot the closing price as a time series line chart
bitcoin_data['Close'].plot(title='Bitcoin daily closing price')
plt.show()
```

## Key takeaways

- `parse_dates=True` (with `index_col='Date'`) turns the date column into a `DatetimeIndex`, which
  makes time-series plotting and resampling straightforward.
- Calling `.plot()` on a price series produces a quick line chart of the trend over time.

> Note: exact variable/file names and starter code come from DataCamp's interactive editor; the code
> above is a faithful reconstruction of the expected solution.