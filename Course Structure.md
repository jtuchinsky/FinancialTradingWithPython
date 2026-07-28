# Course Structure — Financial Trading in Python

[DataCamp course](https://campus.datacamp.com/courses/financial-trading-in-python/trading-basics-1?ex=3)
· instructor: Chelsea Yang. 4 chapters, 50 exercises.

Each **chapter** maps to a `lessons/Chapter N - Name/` directory. Only the **video** exercises are
scaffolded, each as a `Topic M - <title>/` folder (numbered sequentially per chapter) containing
`Notes.md`, generated chart PNG(s), and `Exercises.ipynb`. The Video rows below are annotated with
their Topic number; see [CLAUDE.md](CLAUDE.md) for the layout.

## Chapter 1 · Trading Basics → [`lessons/Chapter1 - Trading Basics/`](lessons/Chapter1%20-%20Trading%20Basics/)

| # | Exercise | XP | Type |
|---|----------|----|------|
| 1 | What is financial trading | 50 | Video → Topic 1 |
| 2 | The concept of trading | 50 | Multiple choice |
| 3 | Plot a time series line chart | 100 | Coding |
| 4 | Plot a candlestick chart | 100 | Coding |
| 5 | Getting familiar with your trading data | 50 | Multiple choice |
| 6 | Resample the data | 100 | Coding |
| 7 | Plot a return histogram | 100 | Coding |
| 8 | Calculate and plot SMAs | 100 | Coding |
| 9 | Financial trading with bt | 50 | Video → Topic 2 |
| 10 | The bt process | 100 | Coding |
| 11 | Define and backtest a simple strategy | 100 | Coding |

## Chapter 2 · Technical Indicators → [`lessons/Chapter2 - Technical Indicators/`](lessons/Chapter2%20-%20Technical%20Indicators/)

| # | Exercise | XP | Type |
|---|----------|----|------|
| 1 | Trend indicator MAs | 50 | Video → Topic 1 |
| 2 | Calculate and plot two EMAs | 100 | Coding |
| 3 | SMA vs. EMA | 100 | Coding |
| 4 | Strength indicator: ADX | 50 | Video → Topic 2 |
| 5 | Understand the ADX | 50 | Multiple choice |
| 6 | Calculate the ADX | 100 | Coding |
| 7 | Visualize the ADX | 100 | Coding |
| 8 | Momentum indicator: RSI | 50 | Video → Topic 3 |
| 9 | Understand the RSI | 50 | Multiple choice |
| 10 | Calculate the RSI | 100 | Coding |
| 11 | Visualize the RSI | 100 | Coding |
| 12 | Volatility indicator: Bollinger Bands | 50 | Video → Topic 4 |
| 13 | Understand Bollinger Bands | 50 | Multiple choice |
| 14 | Implement Bollinger Bands | 100 | Coding |

## Chapter 3 · Trading Strategies → [`lessons/Chapter3 - Trading Strategies/`](lessons/Chapter3%20-%20Trading%20Strategies/)

| # | Exercise | XP | Type |
|---|----------|----|------|
| 1 | Trading signals | 50 | Video → Topic 1 |
| 2 | Understand trading signals | 50 | Multiple choice |
| 3 | Build an SMA-based signal strategy | 100 | Coding |
| 4 | Build an EMA-based signal strategy | 100 | Coding |
| 5 | Trend-following strategies | 50 | Video → Topic 2 |
| 6 | Construct an EMA crossover signal | 100 | Coding |
| 7 | Build and backtest a trend-following strategy | 100 | Coding |
| 8 | Mean reversion strategy | 50 | Video → Topic 3 |
| 9 | Match the signals with the strategies | 100 | Matching |
| 10 | Construct an RSI based signal | 100 | Coding |
| 11 | Build and backtest a mean reversion strategy | 100 | Coding |
| 12 | Strategy optimization and benchmarking | 50 | Video → Topic 4 |
| 13 | Conduct a strategy optimization | 100 | Coding |
| 14 | Perform a strategy benchmarking | 100 | Coding |

## Chapter 4 · Performance Evaluation → [`lessons/Chapter4 - Performance Evaluation/`](lessons/Chapter4%20-%20Performance%20Evaluation/)

| # | Exercise | XP | Type |
|---|----------|----|------|
| 1 | Strategy return analysis | 50 | Video → Topic 1 |
| 2 | Review return results of a backtest | 100 | Coding |
| 3 | Plot return histograms of a backtest | 100 | Coding |
| 4 | Compare return results of multiple strategies | 100 | Coding |
| 5 | Drawdown | 50 | Video → Topic 2 |
| 6 | Review performance with drawdowns | 100 | Coding |
| 7 | Calculate and review the Calmar ratio | 100 | Coding |
| 8 | Sharpe ratio and Sortino ratio | 50 | Video → Topic 3 |
| 9 | Evaluate strategy performance by Sharpe ratio | 100 | Coding |
| 10 | Evaluate strategy performance by Sortino ratio | 100 | Coding |
| 11 | Congratulations! | 50 | Video |

## Themes by chapter

- **Ch. 1 — Trading Basics:** load/inspect/visualize price data (line & candlestick charts,
  resampling, return histograms, SMAs) and run a first backtest with the `bt` library.
- **Ch. 2 — Technical Indicators:** trend (SMA/EMA), strength (ADX), momentum (RSI), and volatility
  (Bollinger Bands) indicators.
- **Ch. 3 — Trading Strategies:** turn indicators into signals; build/backtest trend-following and
  mean-reversion strategies; optimize and benchmark them.
- **Ch. 4 — Performance Evaluation:** analyze returns, drawdowns, and risk-adjusted ratios (Calmar,
  Sharpe, Sortino).